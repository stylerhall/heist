from pathlib import Path

from heist import expense, finance, settings, sheet
from heist.finance import TransactionType


def main() -> None:
    """Extracts and writes transaction data to CSV files."""
    statements: Path = settings['statements']
    statements.mkdir(parents=True, exist_ok=True)

    # batch all transactions from multiple lenders into a list
    transactions: list[TransactionType] = expense.get_chase_checking(statements.joinpath("chase"))
    transactions.extend(expense.get_chase_amazon(statements.joinpath("amazon")))
    transactions.extend(expense.get_barclays_arrivalplus(statements.joinpath("barclays")))

    # wildcard search for transactions using a string or list of strings
    vehicle_reg: list[dict] = finance.search_transactions("dmv", transactions)
    amazon: list[dict] = finance.search_transactions(["amazon", "amzn"], transactions)
    apple: list[dict] = finance.search_transactions("apple.com", transactions)
    google: list[dict] = finance.search_transactions("google", transactions)
    subscriptions: list[dict] = finance.search_transactions(["netflix", "openai", "hulu", "spotify"], transactions)

    # csv column sort order based on transaction data
    sort_list: list[str] = ["bank", "date", "description", "amount", "miles"]
    sheet.write_csv(statements.joinpath("all_transactions.csv"), transactions, sort_list=sort_list)
    sheet.write_csv(statements.joinpath("vehicle_registration.csv"), vehicle_reg, sort_list=sort_list)
    sheet.write_csv(statements.joinpath("amazon.csv"), amazon, sort_list=sort_list)
    sheet.write_csv(statements.joinpath("apple.csv"), apple, sort_list=sort_list)
    sheet.write_csv(statements.joinpath("google.csv"), google, sort_list=sort_list)
    sheet.write_csv(statements.joinpath("subscriptions.csv"), subscriptions, sort_list=sort_list)


if __name__ == "__main__":
    main()
