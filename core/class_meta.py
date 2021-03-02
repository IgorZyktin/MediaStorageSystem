# -*- coding: utf-8 -*-

"""Metarecord implementation.

Not supposed to be instantiated directly.
"""
from common import utils_common
from core.class_imeta import IMeta


class Meta(IMeta):
    """Metarecord implementation.

    Not supposed to be instantiated directly.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize instance.
        """
        if args:
            raise ValueError(
                f'{type(self).__name__} does not take positional arguments'
            )

        self.__dict__.update(kwargs)

        delta = set(self.__dict__.keys()) ^ set(IMeta.__annotations__.keys())
        if delta:
            weights = {
                attr: num
                for num, attr in enumerate(IMeta.__annotations__.keys())
            }
            sorter = utils_common.make_weight_sorter(weights)
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
