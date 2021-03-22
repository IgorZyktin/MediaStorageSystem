# -*- coding: utf-8 -*-

"""Helper class created to handle pagination.
"""
import math
from typing import Sequence, Tuple, Generator


class Paginator:
    """Helper class created to handle pagination.
    """

    def __init__(self, sequence: Sequence, current_page: int,
                 items_per_page: int) -> None:
        """Initialize instance.
        """
        self.sequence = sequence
        self.current_page = min(current_page, 1)
        self.items_per_page = items_per_page
        self.total_items = len(sequence)

        if items_per_page:
            self.num_pages = math.ceil(self.total_items / self.items_per_page)
        else:
            self.num_pages = 0

    def __len__(self) -> int:
        """Return total amount of items in sequence.
        """
        return self.total_items

    @property
    def has_previous(self) -> bool:
        """Return True if we can go back.
        """
        return self.current_page > 1

    @property
    def has_next(self) -> bool:
        """Return True if we can go further.
        """
        return self.current_page < self.num_pages

    @property
    def previous_page_number(self) -> int:
        """Return previous page number.
        """
        if self.current_page > 1:
            return self.current_page - 1
        return self.current_page

    @property
    def next_page_number(self) -> int:
        """Return next page number.
        """
        if self.current_page < self.num_pages:
            return self.current_page + 1
        return self.num_pages

    def __iter__(self):
        """Iterate over section.
        """
        stop = self.items_per_page * self.current_page
        if self.current_page == 1:
            start = 0
        else:
            start = stop - self.items_per_page
        return iter(self.sequence[start:stop])

    def iterate_over_pages(self) \
            -> Generator[Tuple[bool, bool, int], None, None]:
        """Iterate over all page numbers.

        First element - is this page is dummy page without number?
        Second element - is this page is current page?
        Third element - page number
        """
        for i in range(1, self.num_pages + 1):
            yield False, i == self.current_page, i

        # TODO - as it is supposed to look
        #  when amount of pages is small
        #  [First] [Previous] [1] [_2_] [3] [4] [5]
        #  when there are lots of pages
        #  [First] [Previous] [1] [_2_] [3] [...] [55] [56] [57] [...] [108]
        #  that sliding windows are actually more complicated that I've
        #  thought at first
