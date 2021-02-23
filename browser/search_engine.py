# -*- coding: utf-8 -*-

"""Instruments related to search and sorting.
"""
import random
import re
from itertools import zip_longest
from typing import List, Iterable, Iterator, Any, Optional, Set

from common.metarecord_class import Metarecord, Metainfo, Pair


class SearchingMachine:
    """Helper class that stores query parameters.
    """
    operators = {'AND', 'OR', 'NOT'}
    string = '|'.join(r'{}'.format(x) for x in operators)
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

    def get_query(self) -> str:
        """Reconstruct query from known arguments.
        """
        return ' '.join([
            *(f'AND {x}' for x in sorted(self.and_)),
            *(f'OR {x}' for x in sorted(self.or_)),
            *(f'NOT {x}' for x in sorted(self.not_)),
        ])


def group_to_size(iterable: Iterable, group_size: int,
                  default: Any = None) -> Iterator[tuple]:
    """Return contents of the iterable grouped in blocks of given size.

    >>> list(group_to_size([1, 2, 3, 4, 5, 6, 7], 2, '?'))
    [(1, 2), (3, 4), (5, 6), (7, '?')]

    >>> list(group_to_size([1, 2, 3, 4, 5, 6, 7], 3, '?'))
    [(1, 2, 3), (4, 5, 6), (7, '?', '?')]
    """
    return zip_longest(*[iter(iterable)] * group_size, fillvalue=default)


def make_searching_machine(query: str) -> SearchingMachine:
    """Make instance of the searching machine for the given query.
    """
    parts = SearchingMachine.pattern.split(query)
    parts = [x.strip() for x in parts if x.strip()]

    instance = SearchingMachine()

    if not parts:
        return instance

    if parts[0] not in SearchingMachine.operators:
        parts.insert(0, 'OR')

    for operator, word in group_to_size(parts, 2):
        if not operator or not word:
            continue

        word = word.lower()

        if operator == 'OR':
            instance.or_.add(word)

        elif operator == 'AND':
            instance.and_.add(word)

        elif operator == 'NOT':
            instance.not_.add(word)

    return instance


def metarecord_pair_sorter(pair: Pair) -> tuple:
    """Rank pair uuid+metarecord according to its internals.
    """
    _, metarecord = pair
    return metarecord_sorter(metarecord)


def metarecord_sorter(metarecord: Metarecord) -> tuple:
    """Rank metarecord according to its internals.
    """
    return (
        metarecord.meta.series,
        metarecord.meta.sub_series,
        metarecord.meta.ordering,
    )


def select_random_images(metainfo: Metainfo,
                         items_per_page: int) -> List[Metarecord]:
    """Return X random metainfo records from metainfo pool.
    """
    # note that size of metainfo in some cases might be smaller
    # than items_per_page and random.sample will throw and exception
    chosen_uuids = random.sample(metainfo.keys(),
                                 min(items_per_page, len(metainfo)))

    chosen_pais = [(uuid, metainfo[uuid]) for uuid in chosen_uuids]

    return get_sorted_metainfo_records(chosen_pais)


def select_images(metainfo: Metainfo, searching_machine, synonyms: dict):
    """Return all metarecords, that match to a given query.
    """
    chosen_pais = []

    and_ = searching_machine.and_
    or_ = searching_machine.or_
    not_ = searching_machine.not_

    for uuid, meta in metainfo.items():
        tags = meta.get_extended_tags_set(synonyms)

        # condition for and - all words must be present
        # condition for or - at least one word must be present
        # condition for not - no words must be present
        # skipped if predicate is empty
        cond_and_ = any((and_ & tags == and_, len(and_) == 0))
        cond_or_ = any((or_ & tags, len(or_) == 0))
        cond_not_ = any((not (not_ & tags), len(not_) == 0))

        if all((cond_and_, cond_or_, cond_not_)):
            chosen_pais.append((uuid, meta))

    return get_sorted_metainfo_records(chosen_pais)


def get_sorted_metainfo_records(pairs: List[Pair]) -> List[Metarecord]:
    """From given pairs of uuid+metarecord return sorted list of metarecords.
    """
    pairs.sort(key=metarecord_pair_sorter)
    return [metarecord for _, metarecord in pairs]
