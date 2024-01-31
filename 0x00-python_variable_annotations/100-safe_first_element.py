#!/usr/bin/env python3
"""Basic annotations and types."""

from typing import Any, Sequence, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Gets the first element of list sequence if any exists."""

    if lst:
        return lst[0]
    else:
        return None
