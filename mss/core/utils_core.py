# -*- coding: utf-8 -*-

"""Utils for core functionality.
"""
import random
from typing import List

from mss import constants
from mss.core.abstract_types.class_abstract_meta import AbstractMeta
from mss.core.abstract_types.class_abstract_repository import (
    AbstractRepository
)
from mss.core.simple_types.class_theme import Theme


def select_random_records(theme: Theme,
                          repository: AbstractRepository,
                          amount: int) -> List[AbstractMeta]:
    """Return X random records from repository.
    """
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

    # note that size of the repository in some cases might be smaller
    # than amount and random.sample will throw and exception
    adequate_amount = min(amount, len(valid_records))
    chosen_records = random.sample(valid_records, adequate_amount)
    chosen_records.sort()

    return chosen_records
