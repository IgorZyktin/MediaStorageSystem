# -*- coding: utf-8 -*-

"""Special utils created to work with text.
"""
from typing import Union

__all__ = [
    'byte_count_to_text',
    'sep_digits',
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


def sep_digits(number: Union[int, float, str], precision: int = 2) -> str:
    """Return number as string with separated thousands.

    >>> sep_digits('12345678')
    '12345678'

    >>> sep_digits(12345678)
    '12 345 678'

    >>> sep_digits(1234.5678)
    '1 234.57'

    >>> sep_digits(1234.5678, precision=4)
    '1 234.5678'
    """
    if isinstance(number, int):
        result = '{:,}'.format(number).replace(',', ' ')

    elif isinstance(number, float):
        if precision == 0:
            result = '{:,}'.format(
                int(round(number, precision))
            ).replace(',', ' ')

        else:
            result = '{:,}'.format(
                round(number, precision)
            ).replace(',', ' ')

        if '.' in result:
            tail = result.rsplit('.')[-1]
            result += '0' * (precision - len(tail))

    else:
        result = str(number)

    return result
