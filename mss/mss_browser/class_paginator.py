# -*- coding: utf-8 -*-

"""Helper class created to handle pagination.
"""
import math
from typing import Sequence, Generator, Dict, Union


class Paginator:
    """Helper class created to handle pagination.
    """

    def __init__(self, sequence: Sequence, current_page: int,
                 items_per_page: int, max_pages_in_block: int = 5) -> None:
        """Initialize instance."""
        assert items_per_page
        self._sequence = sequence
        self._current_page = max(current_page, 1)
        self._max_pages_in_block = max_pages_in_block

        self.total_items = len(sequence)
        self.items_per_page = items_per_page
        self.num_pages = math.ceil(self.total_items / self.items_per_page)

    def __len__(self) -> int:
        """Return total amount of items in the sequence."""
        return self.total_items

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

    def __iter__(self):
        """Iterate over current page."""
        stop = self.items_per_page * self._current_page
        if self._current_page == 1:
            start = 0
        else:
            start = stop - self.items_per_page
        return iter(self._sequence[start:stop])

    def iterate_over_pages(self) \
            -> Generator[Dict[str, Union[int, bool]], None, None]:
        """Iterate over all page numbers.

        First element - is this page is dummy page without number?
        Second element - is this page is current page?
        Third element - page number
        """
        if self.num_pages >= (self._max_pages_in_block * 3 + 2):
            # [1][2][3][...][55][56][57][...][108]
            return self._iterate_long()

        # [1] [2] [3] [4] [5]
        return self._iterate_short()

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

        gen = range(1, self._max_pages_in_block + 1)
        head = _generate(gen)

        middle = self.num_pages // 2
        left = middle - self._max_pages_in_block // 2
        right = left + self._max_pages_in_block
        gen = range(left, right)
        body = _generate(gen)

        gen = range(self.num_pages - self._max_pages_in_block + 1,
                    self.num_pages + 1)
        tail = _generate(gen)

        yield from head
        yield {'is_dummy': True, 'is_current': False, 'number': -1}
        yield from body
        yield {'is_dummy': True, 'is_current': False, 'number': -1}
        yield from tail
