#!/usr/bin/env python3
"""Basic annotations and types."""

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Sums up a list of integers and floating-point numbers."""

    return float(sum(mxd_lst))
