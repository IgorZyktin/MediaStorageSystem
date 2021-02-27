# -*- coding: utf-8 -*-

"""Metarecord interface.

Used to declare all required fields and their types.
"""
from typing import List


class IMeta:
    """Metarecord interface.
    """
    uuid: str

    # content locations
    path_to_content: str
    path_to_preview: str
    path_to_thumbnail: str

    # original file parameters
    original_filename: str
    original_name: str
    original_extension: str

    # search and ordering information
    series: str
    sub_series: str
    ordering: int

    # grouping information
    group_name: str
    group_members: List[str]
    previous_record: str
    next_record: str

    # specific content information
    width: int
    height: int
    resolution: float
    bytes_in_file: int
    seconds: int
    media_type: str

    # information about origin
    registered_at: str
    registered_by_username: str
    registered_by_nickname: str
    author: str
    author_url: str
    origin_url: str
    comment: str

    # tags as a simple sequence
    tags: List[str]

    # identification info
    signature: str
    signature_type: str
