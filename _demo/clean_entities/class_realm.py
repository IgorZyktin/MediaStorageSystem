# -*- coding: utf-8 -*-

"""Collection of themes.
"""
from dataclasses import dataclass, field
from typing import List


# pylint: disable=R0902
@dataclass
class Realm:
    """Collection of themes."""
    uuid: str = ''

    name: str = ''
    label: str = ''

    permissions: List[str] = field(default_factory=list)  # extends
