# -*- coding: utf-8 -*-

"""Utils for core functionality.
"""
import random
from collections import defaultdict
from typing import List

from core.class_abstract_meta import AbstractMeta
from core.class_abstract_repository import AbstractRepository
from mss.utils.utils_collections import arrange_by_alphabet


def calculate_statistics(repository: AbstractRepository,
                         some_old_date: str = '1970-01-01',
                         some_new_date: str = '2040-01-01') -> dict:
    """Return statistics of this repository.
    """
    total_items = len(repository)
    total_size = 0
    min_date = some_new_date
    max_date = some_old_date

    tags_stats = defaultdict(int)
    all_tags = set()

    for record in repository.all_records():
        total_size += record.bytes_in_file
        min_date = min(record.registered_on or min_date, min_date)
        max_date = max(record.registered_on or max_date, max_date)

        for tag in set(record.tags):
            tags_stats[tag] += 1
            all_tags.add(tag)

    sorted_tags = list(tags_stats.items())
    sorted_tags.sort(key=lambda x: x[1], reverse=True)
    tags_by_alphabet = arrange_by_alphabet(all_tags)

    return {
        'total_items': total_items,
        'total_size': total_size,
        'total_tags': len(tags_stats),
        'min_date': min_date,
        'max_date': max_date,
        'tags_stats': dict(tags_stats),
        'sorted_tags': sorted_tags,
        'tags_by_alphabet': tags_by_alphabet,
    }


def select_random_records(repository: AbstractRepository,
                          amount: int) -> List[AbstractMeta]:
    """Return X random records from repository.
    """
    all_known_records = list(repository.all_records())

    # note that size of the repository in some cases might be smaller
    # than amount and random.sample will throw and exception
    adequate_amount = min(amount, len(all_known_records))
    chosen_records = random.sample(all_known_records, adequate_amount)
    chosen_records.sort()

    return chosen_records
