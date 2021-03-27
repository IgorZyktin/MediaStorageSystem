# -*- coding: utf-8 -*-

"""Specific set of resources, grouped by common theme.
"""
from dataclasses import dataclass
from typing import Set

from mss import core


@dataclass
class Theme:
    """Specific set of resources, grouped by common theme.
    """
    name: str
    directory: str
    synonyms: core.Synonyms
    tags_on_demand: core.TagsOnDemand
    statistics: core.ThemeStatistics
    used_uuids: Set[str]

    def __repr__(self) -> str:
        """Return textual representation."""
        return f'{type(self).__name__}<directory={self.directory!r}>'

    def __lt__(self, other) -> bool:
        """Return True if we are less than other."""
        return self.name < other.name
