# -*- coding: utf-8 -*-

"""Storage for themes.
"""
from typing import Dict, Optional, Iterator

from mss import constants
from mss.core.class_theme import Theme


def theme_sorter(theme: Theme) -> str:
    """Sort themes by directory."""
    if theme.directory == constants.ALL_THEMES:
        return ''
    return theme.directory


class ThemesRepository:
    """Storage for themes.
    """

    def __init__(self) -> None:
        """Initialize instance."""
        self._storage_by_directory: Dict[str, Theme] = {}
        self._storage_by_name: Dict[str, Theme] = {}

    def __repr__(self) -> str:
        """Return textual representation."""
        return f'{type(self).__name__}()'

    def __iter__(self) -> Iterator[Theme]:
        """Iterate on themes in the storage."""
        themes = list(self._storage_by_directory.values())
        themes.sort(key=theme_sorter)
        return iter(themes)

    def add(self, theme: Theme) -> None:
        """Add theme to the storage."""
        new_directory = theme.directory not in self._storage_by_directory
        new_name = theme.name not in self._storage_by_name

        if new_directory and new_name:
            self._storage_by_directory[theme.directory] = theme
            self._storage_by_name[theme.name] = theme
            return

        if not new_directory:
            existing = self._storage_by_directory[theme.directory]
            raise KeyError(f'Directory {theme.directory} is '
                           f'already taken for theme {existing}')

        existing = self._storage_by_name[theme.name]
        raise KeyError(f'Name {theme.name} is '
                       f'already taken for theme {existing}')

    def get(self, key: str) -> Optional[Theme]:
        """Return theme by directory."""
        by_directory = self._storage_by_directory.get(key)

        if by_directory is not None:
            return by_directory

        return self._storage_by_name.get(key)
