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

    def __add__(self, other) -> 'Synonyms':
        """Sym two synonyms together."""
        cls = type(self)
        assert isinstance(other, cls), f'Incompatible type: {type(other)}'
        return cls(frozenset(self) | frozenset(other))

    def __eq__(self, other) -> bool:
        """Return True if other has same words."""
        cls = type(self)
        assert isinstance(other, cls), f'Incompatible type: {type(other)}'
        return frozenset(self) == frozenset(other)

    @classmethod
    def from_dict(cls, raw_data: dict) -> 'Synonyms':
        """Create instance from raw data."""
        raw_data = raw_data or {}
        synonyms = [frozenset(words) for words in raw_data.values()]
        return cls(synonyms)
