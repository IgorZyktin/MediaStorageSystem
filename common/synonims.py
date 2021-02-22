# -*- coding: utf-8 -*-

"""Typical synonyms that could improve user experience during search.
"""
from typing import Set

SYNONYMS = [
    {'__testing', '__another_testing'},

    {'bgc', 'bgc2032', 'bgcrisis',
     'bubblegum crisis', 'bubblegum crisis classic'},

    {'bgcrash', 'bubblegum crash', 'bubblegum crash!', 'bgc2033'},

    {'bgc2040', 'bubblegum crisis 2040', 'bubblegum crisis tokyo 2040'},

    {'nene', 'nene romanova', 'romanova'},

    {'priss', 'priss asagiri', 'priss s. asagiri', 'asagiri'},

    {'linna', 'linna yamazaki', 'yamazaki'},

    {'sylia', 'sylia stingray', 'stingray'},
]


def extend_tags_with_synonyms(given_tags: Set[str]) -> None:
    """Mutate given tags by adding synonyms to them.
    """
    for tag in list(given_tags):
        for entry in SYNONYMS:
            if tag in entry:
                given_tags.update(entry)
