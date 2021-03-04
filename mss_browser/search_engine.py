# -*- coding: utf-8 -*-

"""Instruments related to search and sorting.
"""
import random
from itertools import chain
from typing import List

from core.class_imeta import IMeta
from core.class_repository import Repository
from mss_browser.class_search_request import SearchRequest


def select_random_images(repository: Repository,
                         amount: int) -> List[IMeta]:
    """Return X random metainfo records from metainfo pool.
    """
    all_known_records = list(repository)

    # note that size of the repository in some cases might be smaller
    # than amount and random.sample will throw and exception
    adequate_amount = min(amount, len(all_known_records))
    chosen_records = random.sample(all_known_records, adequate_amount)
    chosen_records.sort()

    return chosen_records


def select_images(repository: Repository,
                  search_request: SearchRequest) -> List[IMeta]:
    """Return all metarecords, that match to a given query.
    """
    target_uuids = set()
    and_ = search_request.and_
    or_ = search_request.or_
    not_ = search_request.not_

    for tag in chain(and_, or_, not_):
        target_uuids.update(repository.get_uuids_by_tag(tag))

    chosen_records = []

    for uuid in target_uuids:
        meta = repository.get(uuid)

        if meta is None:
            continue

        tags = repository.get_extended_tags(meta.uuid)

        # condition for and - all words must be present
        # condition for or - at least one word must be present
        # condition for not - no words must be present
        # skipped if predicate is empty
        cond_and_ = any((and_ & tags == and_, len(and_) == 0))
        cond_or_ = any((or_ & tags, len(or_) == 0))
        cond_not_ = any((not (not_ & tags), len(not_) == 0))

        if all((cond_and_, cond_or_, cond_not_)):
            chosen_records.append(meta)

    chosen_records.sort(reverse=search_request.desc)

    return chosen_records
