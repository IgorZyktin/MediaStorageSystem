# -*- coding: utf-8 -*-

"""Storage for themes.
"""
from typing import Dict, Optional, Iterator

from mss import constants
from mss.core.simple_types.class_theme import Theme


def theme_sorter(theme: Theme) -> str:
    """Sort themes by directory."""
    if theme.directory == constants.ALL_THEMES:
        return ''
    return theme.directory


class ThemeRepository:
    """Storage for themes.
    """

    def __init__(self) -> None:
        """Initialize instance."""
        self._storage: Dict[str, Theme] = {}

    def __repr__(self) -> str:
        """Return textual representation."""
        return f'{type(self).__name__}()'

    def __iter__(self) -> Iterator[Theme]:
        """Iterate on themes in the storage."""
        themes = list(self._storage.values())
        themes.sort(key=theme_sorter)
        return iter(themes)

    def add(self, theme: Theme) -> None:
        """Add theme to the storage."""
        if theme.directory not in self._storage:
            self._storage[theme.directory] = theme
            return

        existing = self._storage[theme.directory]
        raise KeyError(f'Directory {theme.directory} is '
                       f'already taken for theme {existing}')

    def get(self, directory: str) -> Optional[Theme]:
        """Return theme by directory."""
        return self._storage.get(directory)
