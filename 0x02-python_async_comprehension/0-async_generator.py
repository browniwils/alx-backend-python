#!/usr/bin/env python3
"""Async Generator."""

import asyncio
import random
import typing


async def async_generator() -> typing.Generator[float, None, None]:
    """Asynchronously wait 1 second and yield a random number."""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
