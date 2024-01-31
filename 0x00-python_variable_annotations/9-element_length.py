#!/usr/bin/env python3
"""Basic annotations and types."""

from typing import Iterable, List, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Return list of tuple with sequence and integer values."""

    return [(i, len(i)) for i in lst]
