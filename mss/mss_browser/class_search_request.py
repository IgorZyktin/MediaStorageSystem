# -*- coding: utf-8 -*-

"""Helper class that stores query parameters.
"""
import re
from typing import TypeVar, Generic, Optional, Set

from mss.utils.utils_collections import group_to_size
from mss import constants

T = TypeVar('T')


class SearchRequest(Generic[T]):
    """Helper class that stores query parameters.
    """
    string = '|'.join(r'{}'.format(x) for x in constants.OPERATORS)
    pattern = re.compile('(' + string + ')')

    def __init__(self,
                 and_: Optional[Set[str]] = None,
                 or_: Optional[Set[str]] = None,
                 not_: Optional[Set[str]] = None):
        """Initialize instance.
        """
        self.and_ = and_ or set()
        self.or_ = or_ or set()
        self.not_ = not_ or set()
        self.desc = False
        self.only_theme = ''
        self.except_theme = ''

    def get_query(self) -> str:
        """Reconstruct query from known arguments.
        """
        sequence = [
            *(f'{constants.KW_AND} {x}' for x in sorted(self.and_)),
            *(f'{constants.KW_OR} {x}' for x in sorted(self.or_)),
            *(f'{constants.KW_NOT} {x}' for x in sorted(self.not_)),
        ]

        if self.desc:
            sequence.append(f'{constants.KW_AND} {constants.FLAG_DESC}')

        return ' '.join(sequence)

    @classmethod
    def from_query(cls, query: str) -> T:
        """Make instance of the searching machine for the given query.
        """
        parts = cls.pattern.split(query)
        parts = [x.strip() for x in parts if x.strip()]

        instance = cls()

        if not parts:
            return instance

        if parts[0] not in constants.OPERATORS:
            parts.insert(0, constants.KW_AND)

        for operator, word in group_to_size(parts, 2):
            if not operator or not word:
                continue

            if word in constants.KEYWORDS:
                if word == constants.FLAG_DESC:
                    instance.desc = True
                else:
                    instance.and_.add(word)
                continue

            word = word.lower()

            if operator == constants.KW_AND:
                instance.and_.add(word)

            elif operator == constants.KW_OR:
                instance.or_.add(word)

            elif operator == constants.KW_NOT:
                instance.not_.add(word)

        return instance
