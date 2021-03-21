# -*- coding: utf-8 -*-

"""Metarecord interface.

Declares all required fields and their types.
Not supposed to be instantiated directly.
"""
from abc import ABC
from typing import List


class AbstractMeta(ABC):
    """Metarecord interface.

    Declares all required fields and their types.
    Not supposed to be instantiated directly.
    """
    uuid: str
    directory: str

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
    registered_on: str
    registered_by_username: str
    registered_by_nickname: str
    author: str
    author_url: str
    origin_url: str
    comment: str

    # identification info
    signature: str
    signature_type: str

    # tags as a simple sequence
    tags: List[str]
