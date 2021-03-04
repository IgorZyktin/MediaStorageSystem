# -*- coding: utf-8 -*-

"""Basic utils.
"""
from itertools import zip_longest
from typing import Dict, Callable, Any, Iterable, Iterator

from colorama import Fore


def make_weight_sorter(weights: Dict[str, int]) -> Callable:
    """Factory for sorter functions.
    """

    def func(element: Any) -> int:
        """Sorter func.
        """
        return weights.get(element, -1)

    return func


def output(*args, color: str = '', **kwargs) -> None:
    """Wrapper for print function.
    """
    if color:
        print(color, *args, Fore.RESET, **kwargs)
    print(*args, **kwargs)


def group_to_size(iterable: Iterable, group_size: int,
                  default: Any = None) -> Iterator[tuple]:
    """Return contents of the iterable grouped in blocks of given size.

    >>> list(group_to_size([1, 2, 3, 4, 5, 6, 7], 2, '?'))
    [(1, 2), (3, 4), (5, 6), (7, '?')]

    >>> list(group_to_size([1, 2, 3, 4, 5, 6, 7], 3, '?'))
    [(1, 2, 3), (4, 5, 6), (7, '?', '?')]
    """
    return zip_longest(*[iter(iterable)] * group_size, fillvalue=default)
