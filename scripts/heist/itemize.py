from pathlib import Path
from typing import Union

from heist import finance, sheet
from heist.finance import TransactionType

__all__: list[str] = [
    "get_chase_checking_transactions",
    "get_chase_amazon_transactions",
    "get_barclays_arrivalplus_transactions"
]


def get_chase_checking_transactions(folder: Union[str, Path]) -> list[TransactionType]:
    """Parses a folder of Chase Bank statements.

    Args:
        folder (str | Path): The folder containing the PDF files.

    Returns:
        (list[dict]) The transaction details.
    """
    folder = Path(folder) if isinstance(folder, str) else folder

    all_trans: list[TransactionType] = []

    for pdf_file in folder.glob("*.pdf"):
        pdf_finance: finance.ChaseChecking = finance.ChaseChecking(pdf_file, save_pdf=False)
        all_trans.extend(pdf_finance.transactions)

    return all_trans


def get_chase_amazon_transactions(folder: Union[str, Path]) -> list[TransactionType]:
    """Parses a folder of Chase Amazon Visa credit card statements.

    Args:
        folder (str | Path): The folder containing the PDF files.

    Returns:
        (list[dict]) The transaction details.
    """
    folder = Path(folder) if isinstance(folder, str) else folder

    all_trans: list[TransactionType] = []

    for pdf_file in folder.glob("*.pdf"):
        pdf_finance: finance.ChaseCreditAmazon = finance.ChaseCreditAmazon(pdf_file, save_pdf=False)
        all_trans.extend(pdf_finance.transactions)

    return all_trans


def get_barclays_arrivalplus_transactions(folder: Union[str, Path]) -> list[TransactionType]:
    """Parses a folder of Barclay's Arrival+ Mastercard credit card statements.

    Args:
        folder (str | Path): The folder containing the PDF files.

    Returns:
        (list[dict]) The transaction details.
    """
    folder = Path(folder) if isinstance(folder, str) else folder

    all_trans: list[TransactionType] = []

    for pdf_file in folder.glob("*.pdf"):
        pdf_finance: finance.BarclaysArrivalPlus = finance.BarclaysArrivalPlus(pdf_file, save_pdf=False)
        all_trans.extend(pdf_finance.transactions)

    return all_trans
