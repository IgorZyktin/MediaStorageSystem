# -*- coding: utf-8 -*-

"""Special utils created to work with text.
"""
from typing import Union

__all__ = [
    'byte_count_to_text',
]

SUFFIXES = {
    'B': 'B', 'kB': 'kB', 'MB': 'MB', 'GB': 'GB', 'TB': 'TB',
    'PB': 'PB', 'EB': 'EB', 'KiB': 'KiB', 'MiB': 'MiB',
    'GiB': 'GiB', 'TiB': 'TiB', 'PiB': 'PiB', 'EiB': 'EiB'
}


def byte_count_to_text(total_bytes: Union[int, float]) -> str:
    """Convert amount of bytes into human readable format.

    >>> byte_count_to_text(1023)
    '1023 B'
    """
    prefix = ''

    if total_bytes < 0:
        prefix = '-'
        total_bytes = abs(total_bytes)

    if total_bytes < 1024:
        return f'{prefix}{int(total_bytes)} ' + SUFFIXES['B']

    total_bytes /= 1024

    if total_bytes < 1024:
        return f'{prefix}{total_bytes:0.1f} ' + SUFFIXES['KiB']

    total_bytes /= 1024

    if total_bytes < 1024:
        return f'{prefix}{total_bytes:0.1f} ' + SUFFIXES['MiB']

    total_bytes /= 1024

    if total_bytes < 1024:
        return f'{prefix}{total_bytes:0.1f} ' + SUFFIXES['GiB']

    total_bytes /= 1024

    if total_bytes < 1024:
        return f'{prefix}{total_bytes:0.1f} ' + SUFFIXES['TiB']

    return (f'{total_bytes / 1024 / 1024 :0.1f} '
            + SUFFIXES['EiB'])
