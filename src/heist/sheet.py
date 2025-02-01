import csv
from pathlib import Path

from heist import logger
from heist.finance import TransactionType

_logger = logger.get(__name__)


def get_fields(data: list[dict], sort_list: list[str] | None) -> list[str]:
    """Gets the fields from the data.

    Args:
        data (list[dict]): The data to get the fields from.
        sort_list (list[str], optional):  The list of fields to sort by. Default is None.

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


def write_csv(filename: str | Path, data: list[TransactionType], sort_list: list[str] | None = None) -> Path:
    """Writes the PDF data to a CSV file.

    Args:
        data (list[dict]): The data to write to the CSV file.
        filename (str | Path): The name of the CSV file.
        sort_list (list[str], optional):  The list of fields to sort by. Default is None.

    Returns:
        (Path) The path to the CSV file.
    """
    field_names: list[str] = get_fields(data, sort_list=sort_list)

    filename = Path(filename)
    filename.unlink(missing_ok=True)

    _logger.info(f"Write CSV: {filename}")

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_names, restval="null", dialect="excel")

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(data)

    return filename
