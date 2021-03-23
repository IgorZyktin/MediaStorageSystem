# -*- coding: utf-8 -*-

"""Helper class created to handle pagination.
"""
import math
from typing import Sequence, Generator, Dict, Union


class Paginator:
    """Helper class created to handle pagination.
    """

    def __init__(self, sequence: Sequence, current_page: int,
                 items_per_page: int, pages_in_block: int = 15) -> None:
        """Initialize instance."""
        assert items_per_page
        self._sequence = sequence
        self._current_page = max(current_page, 1)
        self._pages_in_block = pages_in_block

        self.total_items = len(sequence)
        self.items_per_page = items_per_page
        self.num_pages = math.ceil(self.total_items / self.items_per_page)

    def __len__(self) -> int:
        """Return total amount of items in the sequence."""
        return self.total_items

    def __iter__(self):
        """Iterate over current page."""
        stop = self.items_per_page * self._current_page
        if self._current_page == 1:
            start = 0
        else:
            start = stop - self.items_per_page
        return iter(self._sequence[start:stop])

    @property
    def has_previous(self) -> bool:
        """Return True if we can go back."""
        return self._current_page > 1

    @property
    def has_next(self) -> bool:
        """Return True if we can go further."""
        return self._current_page < self.num_pages

    @property
    def previous_page_number(self) -> int:
        """Return previous page number."""
        if self._current_page > 1:
            return self._current_page - 1
        return self._current_page

    @property
    def next_page_number(self) -> int:
        """Return next page number."""
        if self._current_page < self.num_pages:
            return self._current_page + 1
        return self.num_pages

    @property
    def current_page(self) -> int:
        """Return current page number."""
        return self._current_page

    @current_page.setter
    def current_page(self, value: int) -> None:
        """Set current page number."""
        if 1 <= value <= self.num_pages:
            self._current_page = value
            return

        raise ValueError(
            f'Unable to set current page at {value}, paginator '
            f'has only {self.num_pages} pages'
        )

    @property
    def is_fitting(self) -> bool:
        """Return True if all pages can be displayed at once."""
        return self.num_pages < self._pages_in_block - 2

    def iterate_over_pages(self) \
            -> Generator[Dict[str, Union[int, bool]], None, None]:
        """Iterate over all page numbers."""
        if self.is_fitting:
            # [1][2][3][4][5]
            return self._iterate_short()

        # [...][55][56][57][...]
        return self._iterate_long()

    def _iterate_short(self) \
            -> Generator[Dict[str, Union[int, bool]], None, None]:
        """Iterate over all page numbers.

        Version, where all pages are displayed.
        """
        for i in range(1, self.num_pages + 1):
            yield {
                'is_dummy': False,
                'is_current': i == self._current_page,
                'number': i,
            }

    def _iterate_long(self) \
            -> Generator[Dict[str, Union[int, bool]], None, None]:
        """Iterate over grouped page numbers.

        Version, where some pages are hidden and dummy pages inserted.
        """

        def _generate(_gen):
            return [{'is_dummy': False,
                     'is_current': x == self._current_page,
                     'number': x} for x in _gen]

        position = self.current_page

        if position + self._pages_in_block // 2 < self.num_pages:
            left = max(position - self._pages_in_block // 2, 1)
            right = min(left + self._pages_in_block - 1, self.num_pages)
        else:
            right = min(position + self._pages_in_block // 2, self.num_pages)
            left = max(right - self._pages_in_block + 1, 1)

        gen = range(left, right + 1)
        pages = _generate(gen)

        if self.current_page > self._pages_in_block // 2 + 1:
            yield {'is_dummy': True, 'is_current': False, 'number': -1}

        yield from pages

        if self.current_page + self._pages_in_block // 2 < self.num_pages:
            yield {'is_dummy': True, 'is_current': False, 'number': -1}
