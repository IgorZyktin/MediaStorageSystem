# -*- coding: utf-8 -*-

"""Specific set of resources, grouped by common theme.
"""
from dataclasses import dataclass
from typing import Set

from mss.core.simple_types.class_synonyms import Synonyms
from mss.core.simple_types.class_tags_on_demand import TagsOnDemand
from mss.core.simple_types.class_theme_statistics import ThemeStatistics


@dataclass
class Theme:
    """Specific set of resources, grouped by common theme.
    """
    name: str
    directory: str
    synonyms: Synonyms
    tags_on_demand: TagsOnDemand
    statistics: ThemeStatistics
    used_uuids: Set[str]

    def __repr__(self) -> str:
        """Return textual representation."""
        return f'{type(self).__name__}<name={self.name!r}>'

    def __lt__(self, other) -> bool:
        """Return True if we are less than other."""
        if isinstance(other, type(self)):
            return self.name < other.name
        return False
