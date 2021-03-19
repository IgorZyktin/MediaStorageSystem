# -*- coding: utf-8 -*-

"""Utils for collection handling.
"""
from collections import defaultdict
from itertools import zip_longest
from typing import Collection, Dict, List, Iterable, Any, Iterator


def arrange_by_alphabet(words: Collection[str],
                        unique: bool = True) -> Dict[str, List[str]]:
    """Group words by first letter.

    >>> arrange_by_alphabet(['best', 'ant', 'art', '25'])
    {'2': ['25'], 'A': ['ant', 'art'], 'B': ['best']}
    """
    cleaned_words = [x.strip().lower() for x in words]
    sorted_words = sorted(x for x in cleaned_words if x)
    arranged_words = defaultdict(list)

    for word in sorted_words:
        first_letter = word[0].upper()
        arranged_words[first_letter].append(word)

    if unique:
        for key in arranged_words:
            arranged_words[key] = list(dict.fromkeys(arranged_words[key]))

    return dict(arranged_words)


def group_to_size(iterable: Iterable, group_size: int,
                  default: Any = None) -> Iterator[tuple]:
    """Return contents of the iterable grouped in blocks of given size.

    >>> list(group_to_size([1, 2, 3, 4, 5, 6, 7], 2, '?'))
    [(1, 2), (3, 4), (5, 6), (7, '?')]

    >>> list(group_to_size([1, 2, 3, 4, 5, 6, 7], 3, '?'))
    [(1, 2, 3), (4, 5, 6), (7, '?', '?')]
    """
    return zip_longest(*[iter(iterable)] * group_size, fillvalue=default)
