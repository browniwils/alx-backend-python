#!/usr/bin/env python3
"""Async Generator."""

import typing

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> typing.List[float]:
    """Generate list of 10 numbers."""
    return [rand async for rand in async_generator()]
