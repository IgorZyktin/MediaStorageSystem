# -*- coding: utf-8 -*-

"""Metarecord implementation.
"""
from typing import Optional, List


class Meta:
    """Metarecord implementation.
    """

    def __init__(self,
                 uuid: str = '',
                 directory: str = '',
                 path_to_content: str = '',
                 path_to_preview: str = '',
                 path_to_thumbnail: str = '',
                 original_filename: str = '',
                 original_name: str = '',
                 original_extension: str = '',
                 series: str = '',
                 sub_series: str = '',
                 ordering: int = 0,
                 group_name: str = '',
                 group_members: Optional[List[str]] = None,
                 previous_record: str = '',
                 next_record: str = '',
                 width: int = 0,
                 height: int = 0,
                 resolution: float = 0.0,
                 bytes_in_file: int = 0,
                 seconds: int = 0,
                 media_type: str = '',
                 registered_on: str = '',
                 registered_by_username: str = '',
                 registered_by_nickname: str = '',
                 author: str = '',
                 author_url: str = '',
                 origin_url: str = '',
                 comment: str = '',
                 signature: str = '',
                 signature_type: str = '',
                 tags: Optional[List[str]] = None) -> None:
        """Initialize instance."""
        self.uuid = uuid
        self.directory = directory

        # content locations
        self.path_to_content = path_to_content
        self.path_to_preview = path_to_preview
        self.path_to_thumbnail = path_to_thumbnail

        # original file parameters
        self.original_filename = original_filename
        self.original_name = original_name
        self.original_extension = original_extension

        # search and ordering information
        self.series = series
        self.sub_series = sub_series
        self.ordering = ordering

        # grouping information
        self.group_name = group_name
        self.group_members: List[str] = group_members or []
        self.previous_record = previous_record
        self.next_record = next_record

        # specific content information
        self.width = width
        self.height = height
        self.resolution = resolution
        self.bytes_in_file = bytes_in_file
        self.seconds = seconds
        self.media_type = media_type

        # information about origin
        self.registered_on = registered_on
        self.registered_by_username = registered_by_username
        self.registered_by_nickname = registered_by_nickname
        self.author = author
        self.author_url = author_url
        self.origin_url = origin_url
        self.comment = comment

        # identification info
        self.signature = signature
        self.signature_type = signature_type

        # tags as a simple sequence
        self.tags: List[str] = tags or []

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
        assert isinstance(other, type(self)), f'Incompatible ' \
                                              f'type: {type(other)}'
        return self.get_ordering() < other.get_ordering()

    def get_ordering(self) -> tuple:
        """Return something that we can sort on.
        """
        return self.series, self.sub_series, self.ordering
