# -*- coding: utf-8 -*-

"""Metarecord implementation.

Not supposed to be instantiated directly.
"""
from typing import Dict, Callable, Any

from mss.core.abstract_types.class_abstract_meta import AbstractMeta


def make_weight_sorter(weights: Dict[str, int]) -> Callable:
    """Factory for sorter functions.
    """

    def func(element: Any) -> int:
        """Sorter func.
        """
        return weights.get(element, -1)

    return func


class Meta(AbstractMeta):
    """Metarecord implementation.

    Not supposed to be instantiated directly.
    """

    def __init__(self, **kwargs) -> None:
        """Initialize instance.
        """
        super().__init__()
        self.__dict__.update(kwargs)

        delta = (set(self.__dict__.keys())
                 ^ set(type(self).__annotations__.keys()))

        if delta:
            weights = {
                attr: num
                for num, attr in enumerate(AbstractMeta.__annotations__.keys())
            }
            sorter = make_weight_sorter(weights)
            attrs = ', '.join(sorted(delta, key=sorter))

            raise AttributeError(
                f'{type(self).__name__} instance has '
                f'unmatched attributes: {attrs}'
            )

    def __repr__(self) -> str:
        """Return textual representation.
        """
        return (
            f'{type(self).__name__}'
            f'<uuid={self.uuid!r}, {self.original_filename!r}>'
        )

    def __lt__(self, other) -> bool:
        """Return True if we are less than other.
        """
        if isinstance(other, type(self)):
            return self.get_ordering() < other.get_ordering()
        return False

    def get_ordering(self) -> tuple:
        """Return something that we can sort on.
        """
        return self.series, self.sub_series, self.ordering
