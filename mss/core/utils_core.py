# -*- coding: utf-8 -*-

"""Utils for core functionality.
"""
import random
from typing import List

from mss.core.abstract_types.class_abstract_meta import AbstractMeta
from mss.core.abstract_types.class_abstract_repository import AbstractRepository


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
