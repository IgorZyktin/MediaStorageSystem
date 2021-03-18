# -*- coding: utf-8 -*-

"""Special utils created to work with text.
"""
from typing import Union


SUFFIXES = {
    'RU': {'B': 'Б', 'kB': 'кБ', 'MB': 'МБ', 'GB': 'ГБ', 'TB': 'ТБ',
           'PB': 'ПБ', 'EB': 'ЭБ', 'KiB': 'КиБ', 'MiB': 'МиБ',
           'GiB': 'ГиБ', 'TiB': 'ТиБ', 'PiB': 'ПиБ', 'EiB': 'ЭиБ'},

    'EN': {'B': 'B', 'kB': 'kB', 'MB': 'MB', 'GB': 'GB', 'TB': 'TB',
           'PB': 'PB', 'EB': 'EB', 'KiB': 'KiB', 'MiB': 'MiB',
           'GiB': 'GiB', 'TiB': 'TiB', 'PiB': 'PiB', 'EiB': 'EiB'},
}


def byte_count_to_text(total_bytes: Union[int, float],
                       language: str = 'EN') -> str:
    """Convert amount of bytes into human readable format.

    >>> byte_count_to_text(1023)
    '1023 B'
    """
    prefix = ''
    if total_bytes < 0:
        prefix = '-'
        total_bytes = abs(total_bytes)

    if total_bytes < 1024:
        suffix = SUFFIXES[language]['B']
        return f'{prefix}{int(total_bytes)} {suffix}'

    total_bytes /= 1024

    if total_bytes < 1024:
        suffix = SUFFIXES[language]['KiB']
        return f'{prefix}{total_bytes:0.1f} {suffix}'

    total_bytes /= 1024

    if total_bytes < 1024:
        suffix = SUFFIXES[language]['MiB']
        return f'{prefix}{total_bytes:0.1f} {suffix}'

    total_bytes /= 1024

    if total_bytes < 1024:
        suffix = SUFFIXES[language]['GiB']
        return f'{prefix}{total_bytes:0.1f} {suffix}'

    total_bytes /= 1024

    if total_bytes < 1024:
        suffix = SUFFIXES[language]['TiB']
        return f'{prefix}{total_bytes:0.1f} {suffix}'

    suffix = SUFFIXES[language]['EiB']
    return f'{total_bytes / 1024 / 1024 :0.1f} {suffix}'


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
