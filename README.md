# Heist

[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3118/)

This package provides tools for extracting financial data from PDF files. The current lending instutions supported are:
- Chase Checking Account
- Chase Amazon Visa
- Barclay's Arrival+ Mastercard

---

# Example Usage

```python
from pathlib import Path

from heist import finance, itemize, sheet
from heist.finance import TransactionType

sheets: list[Path] = []

all_trans: list[TransactionType] = itemize.get_chase_checking_transactions("c:/path/to/pdf/files")
all_trans.extend(itemize.get_chase_amazon_transactions("c:/path/to/pdf/files"))
all_trans.extend(itemize.get_barclays_arrivalplus_transactions("c:/path/to/pdf/files"))

vehicle_reg: list[dict] = finance.search_transactions("dmv", all_trans)
amazon: list[dict] = finance.search_transactions(["amazon", "amzn"], all_trans)
apple: list[dict] = finance.search_transactions("apple.com", all_trans)
google: list[dict] = finance.search_transactions("google", all_trans)
subscriptions: list[dict] = finance.search_transactions(["netflix", "openai", "hulu", "spotify"], all_trans)

csv_folder: Path = Path("c:/path/to/write/csv/files")
csv_folder.mkdir(parents=True, exist_ok=True)

# this list defines the order of columns in the CSV files
sort_list: list[str] = ["bank", "date", "description", "amount", "miles"]

sheets.append(sheet.write_csv(csv_folder.joinpath("all_transactions.csv"), all_trans, sort_list=sort_list))
sheets.append(sheet.write_csv(csv_folder.joinpath("vehicle_registration.csv"), vehicle_reg, sort_list=sort_list))
sheets.append(sheet.write_csv(csv_folder.joinpath("amazon.csv"), amazon, sort_list=sort_list))
sheets.append(sheet.write_csv(csv_folder.joinpath("apple.csv"), apple, sort_list=sort_list))
sheets.append(sheet.write_csv(csv_folder.joinpath("google.csv"), google, sort_list=sort_list))
sheets.append(sheet.write_csv(csv_folder.joinpath("subscriptions.csv"), subscriptions, sort_list=sort_list))
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
