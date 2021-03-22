# -*- coding: utf-8 -*-

"""Fully processed user search request.
"""
from typing import FrozenSet, NamedTuple, Dict, List

from mss import constants


class Query(NamedTuple):
    """Fully processed user search request.
    """
    and_: FrozenSet[str]
    or_: FrozenSet[str]
    not_: FrozenSet[str]
    include: FrozenSet[str]
    exclude: FrozenSet[str]
    flags: FrozenSet[str]

    def __str__(self) -> str:
        """Reconstruct query from known arguments."""
        sequence = [
            *(f'{constants.KW_AND} {x}' for x in sorted(self.and_)),
            *(f'{constants.KW_OR} {x}' for x in sorted(self.or_)),
            *(f'{constants.KW_NOT} {x}' for x in sorted(self.not_)),
            *(f'{constants.KW_INCLUDE} {x}' for x in sorted(self.include)),
            *(f'{constants.KW_EXCLUDE} {x}' for x in sorted(self.exclude)),
            *(f'{constants.KW_AND} {x}' for x in sorted(self.flags)),
        ]
        return ' '.join(sequence)

    def __bool__(self) -> bool:
        """Return True if query has actual words to search."""
        return bool(self.and_ or self.or_)

    def as_dict(self) -> Dict[str, List[str]]:
        """Convert query to dict.

        Added mostly for testing purpose.
        """
        return {
            'and_': sorted(self.and_),
            'or_': sorted(self.or_),
            'not_': sorted(self.not_),
            'include': sorted(self.include),
            'exclude': sorted(self.exclude),
            'flags': sorted(self.flags),
        }
