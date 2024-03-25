from pathlib import Path

from pdfripper.reader import RipPdf

__all__: list[str] = ["read_pdf"]


def read_pdf(pdf_file: Path) -> dict[str, list[str]]:
    """Reads a PDF file and returns a dictionary of pages and their text."""
    ripper: RipPdf = RipPdf(pdf_file)
    return ripper.get_all_text()
