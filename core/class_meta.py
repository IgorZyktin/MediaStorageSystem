# -*- coding: utf-8 -*-

"""Metarecord implementation.
"""

from core.class_imeta import IMeta


class Meta(IMeta):
    """Metarecord implementation.
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
            attrs = ', '.join(sorted(delta))
            raise AttributeError(
                f'Metarecord instance has unmatched attributes: {attrs}'
            )

    def __repr__(self) -> str:
        """Return textual representation.
        """
        return (
            f'{type(self).__name__}'
            f'<uuid={self.uuid}, {self.original_filename!r}>'
        )
