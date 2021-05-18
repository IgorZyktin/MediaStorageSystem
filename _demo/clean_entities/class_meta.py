# -*- coding: utf-8 -*-

"""Metarecord of a single item in the storage.
"""
from dataclasses import dataclass, field
from typing import List


# pylint: disable=R0902
@dataclass
class Meta:
    """Metarecord of a single item in the storage."""
    uuid: str = ''

    # binding parameters
    realm_uuid: str = ''
    theme_uuid: str = ''
    group_uuid: str = ''

    # content locations
    path_to_content: str = ''
    path_to_preview: str = ''
    path_to_thumbnail: str = ''

    # original file parameters
    original_filename: str = ''
    original_extension: str = ''

    # specific content information
    width: int = 0
    height: int = 0
    resolution: float = 0.0
    size: int = 0
    duration: int = 0
    type: str = ''

    # group handling
    ordering: int = 0

    # information about origin
    registered_on: str = ''
    registered_by: str = ''
    author: str = ''
    author_url: str = ''
    origin_url: str = ''
    comment: str = ''

    # identification info
    signature: str = ''
    signature_type: str = ''

    # composite parameters
    tags: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
