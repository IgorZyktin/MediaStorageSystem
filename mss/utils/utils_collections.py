# -*- coding: utf-8 -*-

"""Utils for collection handling.
"""
from collections import defaultdict
from typing import Collection, Dict, List


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
