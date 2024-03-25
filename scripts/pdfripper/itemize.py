from pathlib import Path
from typing import Union

from pdfripper import finance, sheet
from pdfripper.finance import TransactionType

__all__: list[str] = [
    "get_chase_checking_transactions",
    "get_chase_amazon_transactions",
    "get_barclays_arrivalplus_transactions"
]


def get_chase_checking_transactions() -> list[TransactionType]:
    folder: Path = Path(r"D:\iCloudDrive\Taxes\2023\statements\seth-check")

    all_trans: list[TransactionType] = []

    for pdf_file in folder.glob("*.pdf"):
        pdf_finance: finance.ChaseChecking = finance.ChaseChecking(pdf_file, save_pdf=False)
        all_trans.extend(pdf_finance.transactions)

    return all_trans


def get_chase_amazon_transactions() -> list[TransactionType]:
    folder: Path = Path(r"D:\iCloudDrive\Taxes\2023\statements\chase-amazon")

    all_trans: list[TransactionType] = []

    for pdf_file in folder.glob("*.pdf"):
        pdf_finance: finance.ChaseCreditAmazon = finance.ChaseCreditAmazon(pdf_file, save_pdf=False)
        all_trans.extend(pdf_finance.transactions)

    return all_trans


def get_barclays_arrivalplus_transactions() -> list[TransactionType]:
    folder: Path = Path(r"D:\iCloudDrive\Taxes\2023\statements\barclay")

    all_trans: list[TransactionType] = []

    for pdf_file in folder.glob("*.pdf"):
        pdf_finance: finance.BarclaysArrivalPlus = finance.BarclaysArrivalPlus(pdf_file, save_pdf=False)
        all_trans.extend(pdf_finance.transactions)

    return all_trans


def itemize_expenses(csv_folder: Union[str, Path] = None) -> tuple[list[Path], list[dict]]:
    """Parses a folder of Chase Bank statements and returns the transaction details.

    Args:
        csv_folder (str | Path): Optional. The folder to save the CSV files. If None, we do not
            write the CSV files. Default is None.

    Returns:
        (list[dict]) The transaction details.
    """
    sort_list: list[str] = ["bank", "date", "description", "amount", "miles"]

    csv_folder: Path = Path(csv_folder)
    csv_folder.mkdir(parents=True, exist_ok=True)

    sheets: list[Path] = []

    all_trans: list[TransactionType] = get_chase_checking_transactions()
    all_trans.extend(get_chase_amazon_transactions())
    all_trans.extend(get_barclays_arrivalplus_transactions())

    # here's what I earned after taxes
    # riot_dep: list[dict] = finance.search_transactions(["direct dep"], all_trans)
    # calc_dep: float = sum([item["amount"] for item in riot_dep])

    vehicle_reg: list[dict] = finance.search_transactions("dmv", all_trans)
    amazon: list[dict] = finance.search_transactions(["amazon", "amzn"], all_trans)
    newegg: list[dict] = finance.search_transactions("newegg", all_trans)
    apple: list[dict] = finance.search_transactions("apple.com", all_trans)
    google: list[dict] = finance.search_transactions("google", all_trans)
    tech_subscriptions: list[dict] = finance.search_transactions(["netflix", "openai", "hulu", "spotify", "patreon", "onepass"], all_trans)
    misc_tech: list[dict] = finance.search_transactions(["gumroad", "name-cheap"], all_trans)
    food: list[dict] = finance.search_transactions(["doordash", "grubhub", "yelp"], all_trans)
    software: list[dict] = finance.search_transactions(["1pass", "maxon", "topaz labs", "artstation", "gumroad"], all_trans)
    work_games: list[dict] = finance.search_transactions(["nintendo", "steam", "blizzard", "playstation", "gog", "analogue causeway"], all_trans)
    internet: list[dict] = finance.search_transactions(["frontier", "spectrum"], all_trans)
    utilities: list[dict] = finance.search_transactions(["so cal gas", "edison", "ladwp"], all_trans)
    insurance: list[dict] = finance.search_transactions("state farm", all_trans)

    # venmo: list[dict] = finance.search_transactions(["venmo"], all_trans)

    if csv_folder is not None:
        sheets.append(sheet.write_csv(csv_folder.joinpath("all_transactions.csv"), all_trans, sort_list=sort_list))
        sheets.append(sheet.write_csv(csv_folder.joinpath("dmv_vehicle_reg.csv"), vehicle_reg, sort_list=sort_list))
        sheets.append(sheet.write_csv(csv_folder.joinpath("shopping_amazon.csv"), amazon, sort_list=sort_list))
        sheets.append(sheet.write_csv(csv_folder.joinpath("shopping_newegg.csv"), newegg, sort_list=sort_list))
        sheets.append(sheet.write_csv(csv_folder.joinpath("tech_apple.csv"), apple, sort_list=sort_list))
        sheets.append(sheet.write_csv(csv_folder.joinpath("tech_google.csv"), google, sort_list=sort_list))
        sheets.append(sheet.write_csv(csv_folder.joinpath("tech_subscriptions.csv"), tech_subscriptions, sort_list=sort_list))
        sheets.append(sheet.write_csv(csv_folder.joinpath("tech_misc.csv"), misc_tech, sort_list=sort_list))
        sheets.append(sheet.write_csv(csv_folder.joinpath("food_delivery.csv"), food, sort_list=sort_list))
        sheets.append(sheet.write_csv(csv_folder.joinpath("tech_software.csv"), software, sort_list=sort_list))
        sheets.append(sheet.write_csv(csv_folder.joinpath("work_ref_gaming.csv"), work_games, sort_list=sort_list))
        sheets.append(sheet.write_csv(csv_folder.joinpath("bills_internet.csv"), internet, sort_list=sort_list))
        sheets.append(sheet.write_csv(csv_folder.joinpath("bills_utilities.csv"), utilities, sort_list=sort_list))
        sheets.append(sheet.write_csv(csv_folder.joinpath("bills_insurance.csv"), insurance, sort_list=sort_list))

    return sheets, all_trans
