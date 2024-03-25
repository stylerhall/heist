import re
import csv
from io import open
from pathlib import Path
from typing import Optional, Union

__all__: list[str] = [
    "cast_float"
]


def cast_float(text: str, absolute: bool = False) -> float:
    """Casts the given string to a float.

    Args:
        text (str): The string to cast.
        absolute (bool): Optional. Whether to return the absolute value of the float. Default is False.

    Returns:
        (float) The string as a float.
    """
    value: float = float(re.sub(r"[$, _*]", "", text))
    return abs(value) if absolute else value


def replace_ligatures(text: str) -> str:
    """Replaces ligatures with their respective characters.

    Args:
        text (str): The string to replace ligatures in.

    Returns:
        (str) The string with ligatures replaced.
    """
    ligatures: dict[str, str] = {
        "ﬀ": "ff",
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
        "ﬅ": "ft",
        "ﬆ": "st",
        "Ꜳ": "AA",
        "Æ": "AE",
        "ꜳ": "aa",
        "â": "a",
        "€": "E",
        "¢": "c",
        "•": "*",
        "™": "TM",
        "®": "(R)"
    }

    for search, replace in ligatures.items():
        text = text.replace(search, replace)

    return text


def convert_date(date_str: str) -> str:
    """Converts the spelled out/abbreviated date month to a numerical value.

    Args:
        date_str (str): The date string to convert. Example: "Jan 01", "January 01".

    Returns:
        (str) The date with numerals. Example: "01/01".
    """
    values: list[str] = date_str.split(" ")

    if len(values) > 2:
        month, day, year = values[0], values[1], values[2]
    elif len(values) == 2:
        month, day = values[0], values[1]
    else:
        raise ValueError(f"invalid date: {date_str}")

    months: list[str] = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

    # this is a more reliable way to match the month since I cannot guarantee
    # that the month will be abbreviated or fully spelled out.
    regex: re.Pattern = re.compile("|".join(months), flags=re.IGNORECASE)
    find: Optional[re.Match] = regex.match(month)

    if find is None:
        raise ValueError(f"invalid month: {month}")

    return f"{str(months.index(find.group().lower()) + 1).zfill(2)}/{day}"
