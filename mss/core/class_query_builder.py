# -*- coding: utf-8 -*-

"""Helper class that stores query parameters.
"""
import re
from typing import TypeVar, Generic, Type, List, Dict, Set

from mss import constants
from mss.utils.utils_collections import group_to_size

QueryType = TypeVar('QueryType')


class QueryBuilder(Generic[QueryType]):
    """Helper class that makes query instances.
    """
    string = '|'.join(r'\b{}\b'.format(x) for x in constants.OPERATORS)
    pattern = re.compile('(' + string + ')')

    def __init__(self, target_type: Type[QueryType]):
        """Initialize instance."""
        self.target_type = target_type

    def split_request_into_parts(self, query_text: str) -> List[str]:
        """Turn user request into series of words."""
        parts = self.pattern.split(query_text)
        parts = [x.strip() for x in parts if x.strip()]

        if not parts:
            return []

        if parts[0] not in constants.OPERATORS:
            parts.insert(0, constants.KW_OR)

        return parts

    @staticmethod
    def update_flags(word: str, sets: Dict[str, Set[str]]) -> bool:
        """Put new flags in the sets dictionary.

        Return True if word is a flag.
        """
        if word in constants.KEYWORDS:
            if word in constants.FLAGS:
                sets['flags'].add(word)
            else:
                sets['and_'].add(word)
            return True
        return False

    @staticmethod
    def update_sets(operator: str, word: str,
                    sets: Dict[str, Set[str]]) -> None:
        """Put new words in the sets dictionary."""
        word = word.lower()

        if operator == constants.KW_AND:
            sets['and_'].add(word)

        elif operator == constants.KW_OR:
            sets['or_'].add(word)

        elif operator == constants.KW_NOT:
            sets['not_'].add(word)

        elif operator == constants.KW_INCLUDE:
            sets['include'].add(word)

        elif operator == constants.KW_EXCLUDE:
            sets['exclude'].add(word)

    def from_query(self, query_text: str, current_directory: str) -> QueryType:
        """Make instance representing given query."""
        sets = dict(and_=set(),
                    or_=set(),
                    not_=set(),
                    include=set(),
                    exclude=set(),
                    flags=set())

        parts = self.split_request_into_parts(query_text)

        for operator, word in group_to_size(parts, 2, default='?'):
            if operator not in constants.OPERATORS \
                    or word in constants.OPERATORS:
                # something is wrong with this query
                # let's return something that can't be found
                return self.target_type(
                    and_=frozenset([constants.NEVER_FIND_THIS]),
                    or_=frozenset(sets['or_']),
                    not_=frozenset(sets['not_']),
                    include=frozenset(sets['include']),
                    exclude=frozenset(sets['exclude']),
                    flags=frozenset(sets['flags']),
                )

            if self.update_flags(word, sets):
                continue

            self.update_sets(operator, word, sets)

        return self.target_type(and_=frozenset(sets['and_']),
                                or_=frozenset(sets['or_']),
                                not_=frozenset(sets['not_']),
                                include=frozenset(sets['include']),
                                exclude=frozenset(sets['exclude']),
                                flags=frozenset(sets['flags']))
