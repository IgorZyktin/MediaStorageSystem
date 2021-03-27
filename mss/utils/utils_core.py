# -*- coding: utf-8 -*-

"""Utils for core functionality.
"""
import random
from itertools import chain
from typing import List

from mss import constants
from mss import core


def select_random_records(theme: core.Theme,
                          repository: core.Repository,
                          query: core.Query,
                          amount: int) -> List[core.Meta]:
    """Return X random records from repository."""
    # FIXME
    all_known_records = list(repository.all_records())

    if theme.directory != constants.ALL_THEMES:
        all_known_records = [
            x for x in all_known_records
            if x.directory == theme.directory
        ]

    avoid_tags = set(theme.tags_on_demand)
    valid_records = []
    for record in all_known_records:
        tags = repository.get_extended_tags(record.uuid)
        if tags & avoid_tags:
            continue

        valid_records.append(record)

    if query.include:
        valid_records = [
            x for x in valid_records
            if x.directory in query.include
        ]

    if query.exclude:
        valid_records = [
            x for x in valid_records
            if x.directory not in query.exclude
        ]

    # note that size of the repository in some cases might be smaller
    # than amount and random.sample will throw and exception
    adequate_amount = min(amount, len(valid_records))
    chosen_records = random.sample(valid_records, adequate_amount)
    chosen_records.sort()

    return chosen_records


def select_records(theme: core.Theme,
                   repository: core.Repository,
                   query: core.Query) -> List[core.Meta]:
    """Return all records, that match to a given query."""
    target_uuids = set()

    if query:
        for tag in chain(query.and_, query.or_):
            target_uuids.update(repository.get_uuids_by_tag(tag))
    else:
        target_uuids = set(repository.all_uuids())

    chosen_records = []

    if constants.FLAG_DEMAND in query.flags:
        avoid_tags = set()
    else:
        avoid_tags = set(theme.tags_on_demand) - query.and_ - query.or_

    for uuid in target_uuids:
        meta = repository.get_record(uuid)

        if meta is None:
            continue

        tags = repository.get_extended_tags(meta.uuid)

        if tags & avoid_tags:
            continue

        # condition for and - all words must be present
        # condition for or - at least one word must be present
        # condition for not - no words must be present
        # skipped if predicate is empty
        cond_and_ = any((query.and_ & tags == query.and_,
                         len(query.and_) == 0))

        cond_or_ = any((query.or_ & tags,
                        len(query.or_) == 0))

        cond_not_ = any((not (query.not_ & tags),
                         len(query.not_) == 0))

        if all((cond_and_, cond_or_, cond_not_)):
            chosen_records.append(meta)

    if query.include:
        chosen_records = [
            x for x in chosen_records
            if x.directory in query.include
        ]

    if query.exclude:
        chosen_records = [
            x for x in chosen_records
            if x.directory not in query.exclude
        ]

    chosen_records.sort(reverse=constants.FLAG_DESC in query.flags)

    return chosen_records
