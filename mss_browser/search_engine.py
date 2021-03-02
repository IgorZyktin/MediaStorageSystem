# -*- coding: utf-8 -*-

"""Instruments related to search and sorting.
"""
import random
import re
from itertools import zip_longest
from typing import List, Iterable, Iterator, Any, Optional, Set, Tuple

from common.metarecord_class import Metarecord, Metainfo, Meta
from core.class_imeta import IMeta
from core.class_repository import Repository
from core.class_search_enhancer import KEYWORDS


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
        self.desc = False

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

        if word in KEYWORDS:
            instance.and_.add(word)
            if word == 'DESC':
                instance.desc = True
            continue

        word = word.lower()

        if operator == 'OR':
            instance.or_.add(word)

        elif operator == 'AND':
            instance.and_.add(word)

        elif operator == 'NOT':
            instance.not_.add(word)

    return instance


def select_random_images(repository: Repository,
                         amount: int) -> List[Meta]:
    """Return X random metainfo records from metainfo pool.
    """
    all_known_records = list(repository)

    # note that size of the repository in some cases might be smaller
    # than amount and random.sample will throw and exception
    adequate_amount = min(amount, len(all_known_records))
    chosen_records = random.sample(all_known_records, adequate_amount)
    chosen_records.sort()

    return chosen_records


def select_images(repository: Repository, searching_machine) -> List[IMeta]:
    """Return all metarecords, that match to a given query.

    chosen_pais = []

    and_ = searching_machine.and_
    or_ = searching_machine.or_
    not_ = searching_machine.not_

    for meta in metainfo:
        # FIXME
        tags = meta.tags

        # condition for and - all words must be present
        # condition for or - at least one word must be present
        # condition for not - no words must be present
        # skipped if predicate is empty
        cond_and_ = any((and_ & tags == and_, len(and_) == 0))
        cond_or_ = any((or_ & tags, len(or_) == 0))
        cond_not_ = any((not (not_ & tags), len(not_) == 0))

        if all((cond_and_, cond_or_, cond_not_)):
            chosen_pais.append((meta.uuid, meta))

    return get_sorted_metainfo_records(chosen_pais)
    """
    and_uuids = set()
    or_uuids = set()
    not_uuids = set()

    print('and_', searching_machine.and_)
    print('or_', searching_machine.or_)
    print('not_', searching_machine.not_)

    for tag in searching_machine.and_:
        and_uuids.update(repository.get_uuids_by_tag(tag))

    for tag in searching_machine.or_:
        with_this_tag = repository.get_uuids_by_tag(tag)
        for uuid in with_this_tag:
            record = repository.get(uuid)
            if record is not None and set(record.tags) & searching_machine.and_:
                or_uuids.add(record.uuid)

    for tag in searching_machine.not_:
        not_uuids.update(repository.get_uuids_by_tag(tag))

    resulting_uuids = (and_uuids | or_uuids) - not_uuids
    chosen_records = [repository.get(uuid) for uuid in resulting_uuids]
    chosen_records = [x for x in chosen_records if x is not None]
    chosen_records.sort(reverse=searching_machine.desc)

    return chosen_records
