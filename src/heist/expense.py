from pathlib import Path

from heist import finance, logger
from heist.finance import TransactionType

_logger = logger.get(__name__)


def get_chase_checking(folder: str | Path) -> list[TransactionType]:
    """Parses a folder of Chase Bank statements.

    Args:
        folder (str | Path): The folder containing the PDF files.

    Returns:
        (list[dict]) The transaction details.
    """
    folder = Path(folder) if isinstance(folder, str) else folder

    if not folder.exists():
        _logger.error(f"Folder does not exist: {folder}")
        return []

    _logger.info("Read Chase checking statements.")

    all_trans: list[TransactionType] = []

    for pdf_file in folder.glob("*.pdf"):
        pdf_finance: finance.ChaseChecking = finance.ChaseChecking(pdf_file, save_pdf=False)
        all_trans.extend(pdf_finance.transactions)

    return all_trans


def get_chase_amazon(folder: str | Path) -> list[TransactionType]:
    """Parses a folder of Chase Amazon Visa credit card statements.

    Args:
        folder (str | Path): The folder containing the PDF files.

    Returns:
        (list[dict]) The transaction details.
    """
    folder = Path(folder) if isinstance(folder, str) else folder

    if not folder.exists():
        _logger.error(f"Folder does not exist: {folder}")
        return []

    _logger.info("Read Chase Amazon statements.")

    all_trans: list[TransactionType] = []

    for pdf_file in folder.glob("*.pdf"):
        pdf_finance: finance.ChaseCreditAmazon = finance.ChaseCreditAmazon(pdf_file, save_pdf=False)
        all_trans.extend(pdf_finance.transactions)

    return all_trans


def get_barclays_arrivalplus(folder: str | Path) -> list[TransactionType]:
    """Parses a folder of Barclay's Arrival+ Mastercard credit card statements.

    Args:
        folder (str | Path): The folder containing the PDF files.

    Returns:
        (list[dict]) The transaction details.
    """
    folder = Path(folder) if isinstance(folder, str) else folder

    if not folder.exists():
        _logger.error(f"Folder does not exist: {folder}")
        return []

    _logger.info("Read Barclay's Arrival+ statements.")

    all_trans: list[TransactionType] = []

    for pdf_file in folder.glob("*.pdf"):
        pdf_finance: finance.BarclaysArrivalPlus = finance.BarclaysArrivalPlus(pdf_file, save_pdf=False)
        all_trans.extend(pdf_finance.transactions)

    return all_trans
