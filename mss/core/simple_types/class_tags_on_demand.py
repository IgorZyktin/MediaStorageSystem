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

    def __add__(self, other) -> 'TagsOnDemand':
        """Sym two tags holders together."""
        cls = type(self)
        assert isinstance(other, cls), f'Incompatible type: {type(other)}'
        return cls(frozenset(self) | frozenset(other))

    def __eq__(self, other) -> bool:
        """Return True if other has same tags."""
        cls = type(self)
        assert isinstance(other, cls), f'Incompatible type: {type(other)}'
        return frozenset(self) == frozenset(other)

    def __bool__(self) -> bool:
        """Return True if we have at least one tag."""
        return bool(self._storage)

    @classmethod
    def from_dict(cls, raw_data: dict) -> 'TagsOnDemand':
        """Create instance from raw data."""
        raw_data = raw_data or {}
        tags = []
        for words in raw_data.values():
            if isinstance(words, str):
                tags.append(words)
            else:
                tags.extend(words)
        return cls(tags)
