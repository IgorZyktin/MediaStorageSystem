# -*- coding: utf-8 -*-

"""Metarecord implementation."""
from dataclasses import dataclass, field
from typing import List


# pylint: disable=R0902
@dataclass
class Meta:
    """Metarecord implementation."""
    uuid: str = ''
    directory: str = ''  # theme directory

    # content locations
    path_to_content: str = ''
    path_to_preview: str = ''
    path_to_thumbnail: str = ''

    # original file parameters
    original_filename: str = ''
    original_name: str = ''
    original_extension: str = ''

    # search and ordering information
    series: str = ''
    sub_series: str = ''
    ordering: int = 0

    # grouping information
    group_name: str = ''
    group_members: List[str] = field(default_factory=list)
    previous_record: str = ''
    next_record: str = ''

    # specific content information
    width: int = 0
    height: int = 0
    resolution: float = 0.0
    bytes_in_file: int = 0
    seconds: int = 0
    media_type: str = ''

    # information about origin
    registered_on: str = ''
    registered_by_username: str = ''
    registered_by_nickname: str = ''
    author: str = ''
    author_url: str = ''
    origin_url: str = ''
    comment: str = ''

    # identification info
    signature: str = ''
    signature_type: str = ''

    # tags as a simple sequence
    tags: List[str] = field(default_factory=list)

    def __repr__(self) -> str:
        """Return textual representation."""
        return (
            f'{type(self).__name__}'
            f'<uuid={self.uuid!r}, {self.original_filename!r}>'
        )

    def __lt__(self, other) -> bool:
        """Return True if we are less than other."""
        return self.get_ordering() < other.get_ordering()

    def get_ordering(self) -> tuple:
        """Return something that we can sort on."""
        return (
            self.series,
            self.sub_series,
            self.group_name,
            self.ordering,
        )
