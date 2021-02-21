# -*- coding: utf-8 -*-

"""Helper class created to handle pagination.
"""
import math
from typing import Sequence, Tuple, Generator

PAGINATION_WINDOW = 5


class Paginator:
    """Helper class created to handle pagination.
    """
    def __init__(self, sequence: Sequence, current_page: int,
                 items_per_page: int) -> None:
        """Initialize instance.
        """
        assert items_per_page > 0
        self.sequence = sequence
        self.current_page = current_page
        self.items_per_page = items_per_page
        self.total_items = len(sequence)
        self.num_pages = math.ceil(self.total_items / self.items_per_page)

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

    def iterate_over_pages(self)\
            -> Generator[Tuple[bool, bool, int], None, None]:
        """Iterate over all page numbers.

        First element - is this page is dummy page without number?
        Second element - is this page is current page?
        Third element - page number
        """
        # FIXME
        for i in range(1, self.num_pages + 1):
            yield False, i == self.current_page, i

        # if self.num_pages <= PAGINATION_WINDOW * 3:
        # else:
        #     for i in range(1, self.num_pages + 1):
        #         if 1 <= i <= PAGINATION_WINDOW:
        #             yield False, i == self.current_page, i
        #     all_pages = list(range(1, self.num_pages + 1))
        #     left_start = 0
        #     left_stop = PAGINATION_WINDOW + 1
        #
        #     right_start = len(all_pages) - PAGINATION_WINDOW
        #     right_stop = len(all_pages)
        #
        #     center_start = self.current_page - PAGINATION_WINDOW // 2
        #     center_stop = self.current_page + PAGINATION_WINDOW // 2 + 1
        #
        #     center_start = min(1, center_start)
        #     center_stop = min(center_stop, self.num_pages)
        #
        #     for i in range(left_start + 1, left_stop + 1):
        #         yield False, i == self.current_page, i
        #
        #     if left_stop < center_start:
        #         yield True, False, 0
        #         for i in range(center_start + 1, center_stop + 1):
        #             yield False, i == self.current_page, i
        #     else:
        #         for i in range(left_stop + 1, center_stop + 1):
        #             yield False, i == self.current_page, i
        #     #
        #     # if center_stop < right_start:
        #     #     yield True, False, 0
        #     # else:
        #     #     for i in range(center_stop + 1, right_stop + 1):
        #     #         yield False, i == self.current_page, i
