# -*- coding: utf-8 -*-

"""Utils for core functionality.
"""
from collections import defaultdict

from core.class_repository import Repository


def calculate_statistics(repo: Repository,
                         some_old_date: str = '1970-01-01',
                         some_new_date: str = '2040-01-01') -> dict:
    """Return statistics of this repository.
    """
    total_items = len(repo)
    total_size = 0
    min_date = some_new_date
    max_date = some_old_date

    tags_stats = defaultdict(int)

    for record in repo:
        total_size += record.bytes_in_file
        min_date = min(record.registered_at, min_date)
        max_date = max(record.registered_at, max_date)

        for tag in set(record.tags):
            tags_stats[tag] += 1

    return {
        'total_items': total_items,
        'total_size': total_size,
        'min_date': min_date if min_date != some_new_date else '',
        'max_date': max_date if max_date != some_old_date else '',
        'tags_stats': dict(tags_stats),
    }
