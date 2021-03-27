# -*- coding: utf-8 -*-

"""Specific set of resources, grouped by common theme.
"""
from dataclasses import dataclass
from typing import Set

from mss.core.class_synonyms import Synonyms
from mss.core.class_tags_on_demand import TagsOnDemand
from mss.core.class_theme_statistics import ThemeStatistics


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
        return f'{type(self).__name__}<directory={self.directory!r}>'

    def __lt__(self, other) -> bool:
        """Return True if we are less than other."""
        assert isinstance(other, type(self)), f'Incompatible type: ' \
                                              f'{type(other)}'
        return self.name < other.name
