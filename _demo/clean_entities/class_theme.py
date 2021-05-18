# -*- coding: utf-8 -*-

"""Collection of groups.
"""
from dataclasses import dataclass, field
from typing import List, Dict


# pylint: disable=R0902
@dataclass
class Theme:
    """Collection of groups."""
    uuid: str = ''

    name: str = ''
    label: str = ''

    synonyms: Dict[str, str] = field(default_factory=dict)
    tags_on_demand: Dict[str, str] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)  # extends
