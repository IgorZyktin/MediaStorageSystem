# -*- coding: utf-8 -*-

"""Collection of words, used to enhance metainfo tags.
"""
from typing import FrozenSet, Collection, Generator


class Synonyms:
    """Collection of words, used to enhance metainfo tags.
    """

    def __init__(self, synonyms: Collection[Collection[str]]) -> None:
        """Initialize instance."""
        self._storage = tuple(frozenset(x) for x in synonyms)

    def __repr__(self) -> str:
        """Return textual representation."""
        return f'{type(self).__name__}<{len(self._storage)} groups>'

    def __iter__(self) -> Generator[FrozenSet[str], None, None]:
        """Iterate on groups in the storage."""
        for group in self._storage:
            yield group

    @classmethod
    def from_dict(cls, raw_data: dict) -> 'Synonyms':
        """Create instance from raw data."""
        synonyms = [frozenset(words) for words in raw_data.values()]
        return cls(synonyms)
