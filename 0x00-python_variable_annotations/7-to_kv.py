#!/usr/bin/env python3
"""Basic annotations and types."""

from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Converts key value pair to a tuple of the key and
    the square of its value."""

    return (k, float(v**2))
