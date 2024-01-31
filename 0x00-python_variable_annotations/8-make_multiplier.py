#!/usr/bin/env python3
"""Basic annotations and types."""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Returns function."""

    return lambda x: x * multiplier
