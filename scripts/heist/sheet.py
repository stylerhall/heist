import csv
from pathlib import Path
from typing import Optional, Union

from heist.finance import TransactionType

__all__: list[str] = [
    "get_fields",
    "write_csv"
]


def get_fields(data: list[dict], sort_list: Optional[list[str]]) -> list[str]:
    """Gets the fields from the data.

    Args:
        data (list[dict]): The data to get the fields from.
        sort_list (list[str]): Optional. The list of fields to sort by. Default is None.

    Returns:
        (list[str]) The fields from the data sorted to match the sort_list if passed.
    """
    fields: list[str] = []
    for item in data:
        fields.extend(list(item.keys()))

    fields = list(filter(None, set(fields)))

    if sort_list is None:
        return fields

    fields = sorted(fields, key=lambda x: sort_list.index(x) if x in sort_list else len(sort_list))

    return fields


def write_csv(filename: Union[str, Path], data: list[TransactionType], sort_list: Optional[list[str]] = None) -> Path:
    """Writes the PDF data to a CSV file.

    Args:
        data (list[dict]): The data to write to the CSV file.
        filename (str | Path): The name of the CSV file.
        sort_list (list[str]): Optional. The list of fields to sort by. Default is None.

    Returns:
        (Path) The path to the CSV file.
    """
    field_names: list[str] = get_fields(data, sort_list=sort_list)

    filename = Path(filename)
    filename.unlink(missing_ok=True)

    print(f"write csv: {filename}")

    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names, restval="null", dialect="excel")

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(data)

    return filename
