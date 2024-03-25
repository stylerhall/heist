# Heist

[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3118/)

This package provides tools for extracting financial data from PDF files. With this data you may search for specific transactions or write out CSV files for Excel or Google Sheets.

---

# Statement Classes

_Review your PDF file to understand how each transaction line is specified as you will likely need to subclass and create custom regex patterns to fit your statement needs._

The `finance` module contains the base class for financial statements. There are a few examples of sub-classed statements that illustrate how to add new financial institutions.  When subclassing the `StatementBase` class as a new financial statement class, you must implement the `_get_transaction_details()` and `_parse_transaction()` methods.

## Regex Patterns

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


# Example Usage and Searching

```python
from pathlib import Path

from heist import finance, expense, sheet
from heist.finance import TransactionType

# batch all transactions from multiple lenders into a list
transactions: list[TransactionType] = expense.get_chase_checking("c:/path/to/pdf/files")
transactions.extend(expense.get_chase_amazon("c:/path/to/pdf/files"))
transactions.extend(expense.get_barclays_arrivalplus("c:/path/to/pdf/files"))

# wildcard search for transactions using a string or list of strings
vehicle_reg: list[dict] = finance.search_transactions("dmv", transactions)
amazon: list[dict] = finance.search_transactions(["amazon", "amzn"], transactions)
apple: list[dict] = finance.search_transactions("apple.com", transactions)
google: list[dict] = finance.search_transactions("google", transactions)
subscriptions: list[dict] = finance.search_transactions(["netflix", "openai", "hulu", "spotify"], transactions)

# specify and create the csv destination folder
csv_folder: Path = Path("c:/path/to/write/csv/files")
csv_folder.mkdir(parents=True, exist_ok=True)

# csv column sort order based on transaction data
sort_list: list[str] = ["bank", "date", "description", "amount", "miles"]
sheet.write_csv(csv_folder.joinpath("all_transactions.csv"), transactions, sort_list=sort_list)
sheet.write_csv(csv_folder.joinpath("vehicle_registration.csv"), vehicle_reg, sort_list=sort_list)
sheet.write_csv(csv_folder.joinpath("amazon.csv"), amazon, sort_list=sort_list)
sheet.write_csv(csv_folder.joinpath("apple.csv"), apple, sort_list=sort_list)
sheet.write_csv(csv_folder.joinpath("google.csv"), google, sort_list=sort_list)
sheet.write_csv(csv_folder.joinpath("subscriptions.csv"), subscriptions, sort_list=sort_list)
```

---

# Dependencies

- **[PyPDF](https://pypi.org/project/pypdf/)**
- **[Poppler](vendored/poppler/README.md)**

---

# Social

[![github](https://img.shields.io/badge/GitHub-stylerhall-181717.svg?style=flat&logo=github)](https://github.com/stylerhall)
[![twitter](https://img.shields.io/badge/Twitter-@particlevfx-00aced.svg?style=flat&logo=twitter)](https://twitter.com/particlevfx)

---

# Changelist

- 2024-24-03: Initial commit
