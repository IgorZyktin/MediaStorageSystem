# -*- coding: utf-8 -*-

"""Group of one or more metarecords.
"""
from dataclasses import dataclass, field
from typing import List


# pylint: disable=R0902
@dataclass
class Group:
    """Group of one or more metarecords."""
    uuid: str = ''

    # binding parameters
    realm_uuid: str = ''
    theme_uuid: str = ''

    # information about origin
    registered_on: str = ''  # replaces
    registered_by: str = ''  # replaces
    author: str = ''  # replaces
    author_url: str = ''  # replaces
    origin_url: str = ''  # replaces
    comment: str = ''  # replaces

    # composite parameters
    tags: List[str] = field(default_factory=list)  # extends
    permissions: List[str] = field(default_factory=list)  # extends

    # specific group parameters
    hierarchy: List[str] = field(default_factory=list)
    members: List[str] = field(default_factory=list)
