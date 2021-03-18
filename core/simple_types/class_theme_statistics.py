# -*- coding: utf-8 -*-

"""General metainfo on specific theme.
"""
from collections import defaultdict
from typing import List, Dict, Collection, Generator, Tuple, Union, Any

from mss.utils.utils_collections import arrange_by_alphabet
from mss.utils.utils_text import sep_digits, byte_count_to_text


class ThemeStatistics:
    """General metainfo on specific theme.
    """

    def __init__(self) -> None:
        """Initialize instance."""
        self.min_date = ''
        self.max_date = ''
        self.total_items = 0
        self.total_size = 0
        self._tags: List[str] = []
        self._tags_by_popularity: Dict[str, int] = {}
        self._tags_by_alphabet: Dict[str, List[str]] = {}
        self._need_recalculation_popularity = True
        self._need_recalculation_alphabet = True

    def __repr__(self) -> str:
        """Return textual representation."""
        return f'{type(self).__name__}<total_items={self.total_items!r}>'

    def __iter__(self) -> Generator[Tuple[str, Union[int, str]], None, None]:
        """Iterate on pais of parameters, but not nested ones."""
        for key, value in self.as_dict().items():
            if isinstance(value, (int, str)):
                yield key, value

    def add_item(self, item_date: str, item_size: int,
                 item_tags: Collection[str]) -> None:
        """Add information about single item."""
        self.total_items += 1
        self.total_size += item_size
        self.min_date = min(self.min_date or item_date, item_date)
        self.max_date = max(self.max_date or item_date, item_date)
        self._tags.extend(item_tags)
        self._need_recalculation_popularity = True
        self._need_recalculation_alphabet = True

    def as_dict(self) -> Dict[str, Any]:
        """Return statistics as a dictionary."""
        return {
            'Total items': self.total_items_readable,
            'Total size': self.total_size_readable,
            'Oldest item': self.min_date,
            'Newest item': self.max_date,
            'Total tags': len(self.tags_by_popularity),
            'tags_by_popularity': self.tags_by_popularity,
            'tags_by_alphabet': self.tags_by_alphabet,
        }

    @property
    def total_items_readable(self) -> str:
        """Return total items in human readable format."""
        return sep_digits(self.total_items)

    @property
    def total_size_readable(self) -> str:
        """Return total amount of used bytes in human readable format."""
        return byte_count_to_text(self.total_size)

    @property
    def tags_by_popularity(self) -> Dict[str, int]:
        """Return map of tags sorted by popularity.

        Example:
        {
            "tag_1": 25,
            "tag_2": 14,
        }
        """
        if self._need_recalculation_popularity:
            tags_stats = defaultdict(int)
            for tag in self._tags:
                tags_stats[tag] += 1

            self._tags_by_popularity = {
                key: value
                for key, value in sorted(tags_stats.items(),
                                         key=lambda x: x[1],
                                         reverse=True)
            }
            self._need_recalculation_popularity = False

        return self._tags_by_popularity

    @property
    def tags_by_alphabet(self) -> Dict[str, List[str]]:
        """Return map of tags by alphabet.

        Example:
        {
            "A": ["aqua", "azure"],
            "B"": ["bobcat"],
        }
        """
        if self._need_recalculation_alphabet:
            self._tags_by_alphabet = arrange_by_alphabet(self._tags)
            self._need_recalculation_alphabet = False

        return self._tags_by_alphabet
