"""Heist: Bank Statement Classes
This was written in 2024 to parse statements from 2023. There is a possibility that older or future
statements may not parse correctly. This is due to the fact that the PDF format may change over time.
"""
import re
from pathlib import Path

from heist import logger, pdf, utils

_logger = logger.get(__name__)

TransactionType = dict[str, str | float]


class BaseStatement(pdf.PdfFile):
    """Parses a financial statement PDF file for inspection.

    This class is intended to be subclassed by financial institutions. It provides a base class
    for parsing financial statements. The class provides methods for searching transactions and
    parsing transaction details.

    You may override the `__re_page_end__` and `__re_transaction__` attributes to match the
    page end and transaction lines in the PDF. Financial statements may not be formatted the same
    way, so you may need to override these attributes to match the PDF you are working with.
    """

    # this helps us find the absolute bottom of a page
    __re_page_end__: str = r"Page \d+ of \d+"

    # this helps us find transaction lines
    __re_transaction__: str = (
        r"(?P<date>\d+/\d+)\s+"
        r"(?P<desc>.+)\s+"
        r"(?P<amount>.*[\d]+\.[\d]+)\s+"
        r"(?P<balance>[\d\.,\-]+)"
    )

    def __init__(self,
                 filename: str | Path,
                 start_page: int = 1,
                 end_page: int | None = None,
                 page_break: bool = True,
                 save_pdf: bool = True) -> None:
        """Parses a financial statement PDF file for inspection.

        Args:
            filename (str | Path): The path to the PDF file.
            start_page (int, optional):  The page number to start reading text from. Default is 1.
            page_break (bool, optional):  Whether to remove page breaks in the text. Default is True.
            save_pdf (bool, optional):  Whether to save the text file after reading. Default is False.
        """
        super().__init__(filename, start_page=start_page, end_page=end_page, page_break=page_break, save_pdf=save_pdf)

    @property
    def bank_name(self) -> str:
        """Returns the name of the bank."""
        return re.sub(r"(\w)([A-Z])", r"\1 \2", self.__class__.__name__).lower().strip()

    def _is_transaction(self, text: str) -> bool:
        """Checks if the given string is a transaction line.

        Args:
            text (str): The string to check.

        Returns:
            (bool) True if the string is a transaction line, otherwise False.
        """
        text = text.strip().replace("\r", "").replace("\n", "")
        return bool(re.match(self.__re_transaction__, text))

    def _get_transaction_details(self, text: str, absolute: bool = True) -> tuple:
        """Parses a transaction line and returns the details.

        Args:
            text (str): The transaction line to parse.
            absolute (bool, optional):  Whether to return the absolute value of the amount. Default is True.

        Returns:
            (tuple) The transaction details; date, desc, amount, balance.
        """
        raise NotImplementedError

    def _parse_transaction(self, text: str) -> TransactionType:
        """Parses a transaction line and returns the details.

        Args:
            text (str): The transaction line to parse.

        Returns:
            (dict) The transaction details.
        """
        raise NotImplementedError

    def search(self, wildcards: str | list[str], transactions: list[TransactionType] | None = None) -> list[TransactionType]:
        """Finds transactions that match the given wildcard.

        Args:
            wildcards (str | list[str]): The wildcard or wildcards to search for.
            transactions (list[dict]): The transactions to search.

        Returns:
            (list[dict]]) The transactions that match the wildcard.
        """
        wildcards = "|".join(wildcards) if isinstance(wildcards, list) else wildcards
        regex = re.compile(wildcards, flags=re.IGNORECASE)

        transactions = self.transactions if transactions is None else transactions

        return [item for item in transactions if re.search(regex, item["description"])]

    @property
    def transactions(self) -> list[TransactionType]:
        """Parses a bank statement PDF file and prints the transaction details.

        Returns:
            (list[dict]) The transaction details.
        """
        output: list[TransactionType] = []

        for page_num, lines in self.pages.items():
            for line in lines:
                if not self._is_transaction(line):
                    continue
                output.append(self._parse_transaction(line))

        return output


class ChaseChecking(BaseStatement):

    __re_page_end__: str = r"Page \d+ of \d+"

    __re_transaction__: str = (
        r"(?P<date>\d+/\d+)\s+"
        r"(?P<desc>.+)\s+"
        r"(?P<amount>.*[\d]+\.[\d]+)\s+"
        r"(?P<balance>[\d\.,\-]+)"
    )

    def __init__(self,
                 filename: str | Path,
                 start_page: int = 1,
                 end_page: int | None = None,
                 page_break: bool = True,
                 save_pdf: bool = False) -> None:
        """Parses a Chase Bank checking account statement.

        Args:
            filename (str | Path): The path to the PDF file.
            start_page (int, optional):  The page number to start reading text from. Default is 1.
            page_break (bool, optional):  Whether to remove page breaks in the text. Default is True.
            save_pdf (bool, optional):  Whether to save the text file after reading. Default is False.
        """
        super().__init__(filename, start_page=start_page, end_page=end_page, page_break=page_break, save_pdf=save_pdf)

    def _get_transaction_details(self, text: str, absolute: bool = True) -> tuple:
        """Parses a transaction line and returns the details.

        Args:
            text (str): The transaction line to parse.
            absolute (bool, optional):  Whether to return the absolute value of the amount. Default is True.

        Returns:
            (tuple) The transaction details; date, desc, amount, balance.
        """
        match: re.Match = re.match(self.__re_transaction__, text, flags=re.IGNORECASE)

        date: str = match.group("date")
        desc: str = " ".join(list(filter(None, match.group("desc").split(" "))))
        amount: float = utils.cast_float(match.group("amount"), absolute=absolute)
        balance: float = utils.cast_float(match.group("balance"))

        return date, desc, amount, balance

    def _parse_transaction(self, text: str) -> TransactionType:
        """Parses a transaction line and returns the details.

        Args:
            text (str): The transaction line to parse.

        Returns:
            (dict) The transaction details.
        """
        date, desc, amount, balance = self._get_transaction_details(text)
        return dict(zip(["bank", "date", "description", "amount"], [self.bank_name, date, desc, amount]))


class ChaseCreditAmazon(BaseStatement):

    __re_page_end__ = (
        r"(?P<date>\d+/\d+/\d+)\s+"
        r"(?P<page>Page \d+ of \d+)"
    )

    __re_transaction__ = (
        r"(?P<date>\d+/\d+)\s+"
        r"(?P<desc>.+)\s+"
        r"(?P<amount>.*[\d]+\.[\d]+)"
    )

    def __init__(self, filename: str | Path,
                 start_page: int = 1,
                 end_page: int | None = None,
                 page_break: bool = True,
                 save_pdf: bool = False) -> None:
        """Parses a Chase Amazon credit card statement.

        Args:
            filename (str | Path): The path to the PDF file.
            start_page (int, optional):  The page number to start reading text from. Default is 1.
            page_break (bool, optional):  Whether to remove page breaks in the text. Default is True.
            save_pdf (bool, optional):  Whether to save the text file after reading. Default is False.
        """
        super().__init__(filename, start_page=start_page, end_page=end_page, page_break=page_break, save_pdf=save_pdf)

    def _parse_transaction(self, text: str) -> TransactionType:
        """Parses a transaction line and returns the details.

        Args:
            text (str): The transaction line to parse.

        Returns:
            (dict) The transaction details.
        """
        date, desc, amount = self._get_transaction_details(text)
        return dict(zip(["bank", "date", "description", "amount"], [self.bank_name, date, desc, amount]))

    def _get_transaction_details(self, text: str, absolute: bool = True) -> tuple:
        """Parses a transaction line and returns the details.

        Args:
            text (str): The transaction line to parse.
            absolute (bool, optional):  Whether to return the absolute value of the amount. Default is True.

        Returns:
            (tuple) The transaction details; date, desc, amount, balance.
        """
        match: re.Match = re.match(self.__re_transaction__, text, flags=re.IGNORECASE)

        date: str = match.group("date")
        desc: str = " ".join(list(filter(None, match.group("desc").split(" "))))
        amount: float = utils.cast_float(match.group("amount"), absolute=absolute)

        return date, desc, amount


class BarclaysArrivalPlus(BaseStatement):
    __re_page_end__: str = r"Page \d+ of \d+"

    __re_transaction__: str = (
        r"(?P<dateA>\w+ \d{2})\s+"
        r"(?P<dateB>\w+ \d{2})\s+"
        r"(?P<desc>.+)\s+"
        r"(?P<miles>\d+(?:,\d+)?)\s+"
        r"(?P<amount>.*[\d]+\.[\d]+)"
    )

    def __init__(self,
                 filename: str | Path,
                 start_page: int = 1,
                 end_page: int | None = None,
                 page_break: bool = True,
                 save_pdf: bool = False) -> None:
        """Parses a Barclay's Arrival+ credit card statement.

        Args:
            filename (str | Path): The path to the PDF file.
            start_page (int, optional):  The page number to start reading text from. Default is 1.
            page_break (bool, optional):  Whether to remove page breaks in the text. Default is True.
            save_pdf (bool, optional):  Whether to save the text file after reading. Default is False.
        """
        super().__init__(filename, start_page=start_page, end_page=end_page, page_break=page_break, save_pdf=save_pdf)

    def _parse_transaction(self, text: str) -> TransactionType:
        """Parses a transaction line and returns the details.

        Args:
            text (str): The transaction line to parse.

        Returns:
            (dict) The transaction details.
        """
        date, desc, miles, amount = self._get_transaction_details(text)
        return dict(zip(["bank", "date", "description", "miles", "amount"], [self.bank_name, date, desc, miles, amount]))

    def _get_transaction_details(self, text: str, absolute: bool = True) -> tuple:
        """Parses a transaction line and returns the details.

        Args:
            text (str): The transaction line to parse.
            absolute (bool, optional):  Whether to return the absolute value of the amount. Default is True.

        Returns:
            (tuple) The transaction details; date, desc, amount, balance.
        """
        match: re.Match = re.match(self.__re_transaction__, text, flags=re.IGNORECASE)

        date: str = utils.convert_date(match.group("dateA"))
        desc: str = " ".join(list(filter(None, match.group("desc").split(" "))))
        miles: str = match.group("miles")
        amount: float = utils.cast_float(match.group("amount"))

        return date, desc, miles, amount


def search_transactions(wildcards: str | list[str], transactions: list[dict]) -> list[dict]:
    """Finds expenses that match the given wildcard.

    Args:
        wildcards (str | list[str]): The wildcard or wildcards to search for.
        transactions (list[dict]): The transactions to search.

    Returns:
        (list[dict]) The transactions that match the wildcard.
    """
    _logger.info(f"Search transactions for: {wildcards}")

    wildcards = "|".join(wildcards) if isinstance(wildcards, list) else wildcards
    regex = re.compile(wildcards, flags=re.IGNORECASE)

    return [item for item in transactions if re.search(regex, item["description"])]
