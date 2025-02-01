# heist

[![python](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3118/)[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

This package provides tools for extracting financial data from PDF files. With this data you may search for specific transactions or write out CSV files for Excel or Google Sheets.

---

# Dependencies

- **[PyYAML](https://pypi.org/project/PyYAML/)**
- **[PyPDF](https://pypi.org/project/pypdf/)**
- **[Poppler (pdftotext.exe)](https://github.com/oschwartz10612/poppler-windows)**

---

# Bank Statement Classes

_Review your PDF file to understand how each transaction line is specified as you will likely need to subclass and create custom regex patterns to fit your statement needs._

The `finance` module contains the base class for financial statements. There are a few examples of sub-classed statements that illustrate how to add new financial institutions.  When subclassing the `StatementBase` class as a new financial statement class, you must implement the `_get_transaction_details()` and `_parse_transaction()` methods.

## Transaction Regex Patterns

Statement classes also have two regex attributes which define the pdf transaction formatting `__re_page_end__` and `__re_transaction__`

The pattern for extracting the date, description, amount, and balance would look something like this:

    03/25       Example charge description                -10.00         123.45

```python
__re_transaction__: str = (
    r"(?P<date>\d+/\d+)\s+"
    r"(?P<desc>.+)\s+"
    r"(?P<amount>.*[\d]+\.[\d]+)\s+"
    r"(?P<balance>[\d\.,\-]+)"
)
```

---


# Configuration Settings (yaml)

The `settings.yaml` file contains the following configuration settings:

- `pdftotext`: The path to the `pdftotext` executable.
- `statements`: The directory where the PDF statements are located.

To use the settings in your scripts:

```python
from heist import settings

print(settings['pdftotext'])
print(settings['statements'])
```

# Example Usage and Searching

```python
from pathlib import Path

from heist import expense, finance, settings, sheet
from heist.finance import TransactionType


def main() -> None:
    """Extracts and writes transaction data to CSV files."""
    statements: Path = settings['statements']
    statements.mkdir(parents=True, exist_ok=True)

    # batch all transactions from multiple lenders into a list
    transactions: list[TransactionType] = expense.get_chase_checking(statements.joinpath("chase"))

    # wildcard search for transactions using a string or list of strings
    subscriptions: list[dict] = finance.search_transactions(["netflix", "openai", "hulu", "spotify"], transactions)

    # csv column sort order based on transaction data
    sort_list: list[str] = ["bank", "date", "description", "amount", "miles"]
    sheet.write_csv(statements.joinpath("subscriptions.csv"), subscriptions, sort_list=sort_list)
```

---

# Social

[![github](https://img.shields.io/badge/GitHub-stylerhall-181717.svg?style=flat&logo=github)](https://github.com/stylerhall)
[![twitter](https://img.shields.io/badge/Twitter-@particlevfx-00aced.svg?style=flat&logo=twitter)](https://twitter.com/particlevfx)

---

# Changelist

- 2025-02-01:
  - Set up the project to use `uv` and `ruff`.
  - Added yaml configuration settings.

- 2024-03-24: Initial commit
