# -*- coding: utf-8 -*-

"""Helper class that stores query parameters.
"""
import re
from typing import TypeVar, Generic, Type

from mss import constants
from mss.utils.utils_collections import group_to_size

T = TypeVar('T')


class QueryBuilder(Generic[T]):
    """Helper class that makes query instances.
    """
    string = '|'.join(r'\b{}\b'.format(x) for x in constants.OPERATORS)
    pattern = re.compile('(' + string + ')')

    def __init__(self, target_type: Type[T]):
        """Initialize instance."""
        self.target_type = target_type

    def from_query(self, query_text: str, current_directory: str) -> T:
        """Make instance representing given query."""
        and_ = set()
        or_ = set()
        not_ = set()
        include = set()
        exclude = set()
        flags = set()

        parts = self.pattern.split(query_text)
        parts = [x.strip() for x in parts if x.strip()]

        if current_directory != constants.ALL_THEMES:
            include.add(current_directory)

        almost_empty_query = self.target_type(
            and_=frozenset(and_),
            or_=frozenset(or_),
            not_=frozenset(not_),
            include=frozenset(include),
            exclude=frozenset(exclude),
            flags=frozenset(flags),
        )

        if not parts:
            return almost_empty_query

        if parts[0] not in constants.OPERATORS:
            parts.insert(0, constants.KW_AND)

        for operator, word in group_to_size(parts, 2, default='?'):
            if operator not in constants.OPERATORS \
                    or word in constants.OPERATORS:
                # something is wrong with this query
                # let's return something that can't be found
                return self.target_type(
                    and_=frozenset([constants.NEVER_FIND_THIS]),
                    or_=frozenset(or_),
                    not_=frozenset(not_),
                    include=frozenset(include),
                    exclude=frozenset(exclude),
                    flags=frozenset(flags),
                )

            if word in constants.KEYWORDS:
                if word in constants.FLAGS:
                    flags.add(word)
                else:
                    and_.add(word)
                continue

            word = word.lower()

            if operator == constants.KW_AND:
                and_.add(word)

            elif operator == constants.KW_OR:
                or_.add(word)

            elif operator == constants.KW_NOT:
                not_.add(word)

            elif operator == constants.KW_INCLUDE:
                include.add(word)

            elif operator == constants.KW_EXCLUDE:
                exclude.add(word)

        return self.target_type(
            and_=frozenset(and_),
            or_=frozenset(or_),
            not_=frozenset(not_),
            include=frozenset(include),
            exclude=frozenset(exclude),
            flags=frozenset(flags),
        )
