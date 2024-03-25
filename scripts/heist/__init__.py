import re
import subprocess
from io import open
from pathlib import Path
from typing import Optional, Union

import pypdf

from heist import utils

__all__: list[str] = ["PdfFile"]


# this is the path to the pdftotext executable from poppler
_pdf_to_text: Path = Path(__file__).parents[2].joinpath("vendored", "poppler", "Library", "bin", "pdftotext.exe")


class PdfFile:
    """Parses a PDF file for inspection.

    We use the pdftotext executable from poppler to extract the text from the PDF. This allows us to
    inspect the text and extract the information we need. The text is then stored in a dictionary
    object, where the keys are the page numbers and the values are the text from the page.
    """

    _filename: Path
    _start: int
    _end: int
    _breaks: bool
    _save_pdf: bool

    # this helps us find the absolute bottom of a page
    __re_page_end__: str = r"Page \d+ of \d+"

    def __init__(self,
                 filename: Union[str, Path],
                 start_page: int = 1,
                 end_page: Optional[int] = None,
                 page_break: bool = True,
                 save_pdf: bool = False) -> None:
        """Parses a PDF file for inspection.

        Args:
            filename (str | Path): The path to the PDF file.
            start_page (int): Optional. The page number to start reading text from. Default is 1.
            page_break (bool): Optional. Whether to remove page breaks in the text. Default is True.
            save_pdf (bool): Optional. Whether to save the text file after reading. Default is False.
        """
        if not _pdf_to_text.is_file():
            raise FileNotFoundError("'pdftotext.exe' could not be found. check out the './vendored/poppler/README.md' file for more info.")

        self._filename = Path(filename)

        if not self._filename.suffix.lower() == ".pdf":
            raise ValueError(f"file is not a PDF: {self._filename}")

        if not self._filename.is_file():
            raise FileNotFoundError(f"file not found: {self._filename}")

        print(f"loading pdf: {self._filename}")
        self._pdf: pypdf.PdfReader = pypdf.PdfReader(self._filename)

        end_page = self.page_count if end_page is None else end_page

        if start_page > end_page:
            raise ValueError(f"start page cannot be greater than the end page - start_page={start_page}, end_page={end_page}, page_count={self.page_count}")

        self._filename = filename
        self._start = start_page
        self._end = end_page
        self._breaks = page_break
        self._save_pdf = save_pdf

    def __repr__(self) -> str:
        info: dict = {
            "pdf_file": self.pdf_file,
            "page_count": self.page_count,
            "start_page": self._start,
            "end_page": self._end,
            "text_file": self.text_file
        }

        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in info.items()])})"

    @property
    def pdf_file(self) -> Path:
        """Returns the associated PDF file."""
        return self._filename

    @property
    def text_file(self) -> Path:
        """The path to the text file that is created when extracting text with poppler.

        Returns:
            (Path) The path to the text file.
        """
        return self.pdf_file.with_suffix(".txt")

    # noinspection PyProtectedMember
    @property
    def page_count(self) -> int:
        """The number of pages in the PDF.

        Returns:
            (int) The number of pages in the PDF.
        """
        return self._pdf._get_num_pages()

    @property
    def pages(self) -> dict[str, list[str]]:
        """Gets the text from the PDF as a dictionary.

        Returns:
            (dict[str, list[str]]) The text from the PDF.
        """
        return self. _text_to_dict()

    def _is_page_end(self, text: str) -> bool:
        return bool(re.search(self.__re_page_end__, text, flags=re.IGNORECASE))

    def dump_text_file(self) -> Path:
        """Dump the text from the PDF to a text file.

        Returns:
            (Path) The path to the text file.
        """
        if not self.pdf_file.exists():
            raise FileNotFoundError(f"file not found: {self.pdf_file}")

        if self._start > self._end:
            raise ValueError(f"the pdf only has {self.page_count} pages. - start_page={self._start}")

        self.text_file.unlink(missing_ok=True)

        command: list[str] = [
            _pdf_to_text.as_posix(),
            "-f", str(self._start),
            "-l", str(self._end),
            "-layout",
            "-enc", "UTF-8",
            "-eol", "dos"
        ]

        if self._breaks:
            command.append("-nopgbrk")

        command.extend([self.pdf_file.as_posix(), self.text_file.as_posix()])
        subprocess.run(command)

        if self._save_pdf:
            print(f"text file: {self.text_file}")

        return self.text_file

    def _text_to_list(self) -> list[str]:
        """Converts the PDF text to a list of strings.

        Details:
            This method will delete the existing text file if it exists, then create a new one.

        Args:
            delete (bool): Optional. Whether to delete the text file after reading. Default is True.

        Returns:
            (list[str]) The text from the file.
        """
        self.dump_text_file()

        if not self.text_file.is_file():
            raise FileNotFoundError(f"file not found: {self.text_file}")

        with open(self.text_file, "r", encoding="utf8") as f:
            lines: list[str] = list(filter(None, [utils.replace_ligatures(line.strip("\n")).lstrip() for line in f.readlines()]))

        return lines

    def _text_to_dict(self) -> dict[str, list[str]]:
        """Converts the PDF text to a dictionary of pages and their text.

        Returns:
            (dict[str, list[str]]) The text from the file.
        """
        text: list[str] = self._text_to_list()

        dict_pages: dict[str, list[str]] = {}
        page_blocks: list[tuple[int, int]] = []

        start_index: Optional[int] = 0

        # the first iteration of the text determines the page breaks, this allows us to
        # split the lines into logical pages, within the dictionary object.
        for i, line in enumerate(text):
            if not self._is_page_end(line):
                continue

            page_blocks.append((start_index, i))
            start_index = i + 1

        # the second iteration runs over the page blocks we created in the first iteration.
        # this allows us to inject the text blocks into the correct pages.
        for i, pages in enumerate(page_blocks):
            start, end = pages
            dict_pages.setdefault(str(i+1), text[start:end])

        if not self._save_pdf:
            self.text_file.unlink(missing_ok=True)

        return dict_pages
