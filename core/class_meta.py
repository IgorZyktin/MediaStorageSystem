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

    def __repr__(self) -> str:
        """Return textual representation.
        """
        return (
            f'{type(self).__name__}'
            f'<uuid={self.uuid}, {self.original_filename!r}>'
        )
