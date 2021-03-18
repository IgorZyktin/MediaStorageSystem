# -*- coding: utf-8 -*-

"""Collection of tags user wants to stash.
"""
from typing import Generator, Collection


class TagsOnDemand:
    """Collection of tags user wants to stash.
    """

    def __init__(self, tags: Collection[str]) -> None:
        """Initialize instance."""
        self._storage = frozenset(tags)

    def __repr__(self) -> str:
        """Return textual representation."""
        return f'{type(self).__name__}({sorted(self._storage)})'

    def __iter__(self) -> Generator[str, None, None]:
        """Iterate on tags in the storage."""
        return (x for x in sorted(self._storage))

    def __contains__(self, item: str) -> bool:
        """Return True if this tag is in out storage."""
        return item in self._storage

    @classmethod
    def from_dict(cls, raw_data: dict) -> 'TagsOnDemand':
        """Create instance from raw data."""
        tags = []
        for words in raw_data.values():
            if isinstance(words, str):
                tags.append(words)
            else:
                tags.extend(words)
        return cls(tags)
