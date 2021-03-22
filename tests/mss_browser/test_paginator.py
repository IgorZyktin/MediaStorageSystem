# -*- coding: utf-8 -*-

"""Tests.
"""
from string import ascii_uppercase

import pytest

from mss.mss_browser.class_paginator import Paginator


@pytest.fixture
def paginator():
    return Paginator(
        sequence=ascii_uppercase,
        current_page=1,
        items_per_page=3,
    )


def test_paginator_creation(paginator):
    assert paginator
    assert len(paginator) == len(ascii_uppercase)


def test_paginator_set_page(paginator):
    assert paginator.current_page == 1
    paginator.current_page = 4
    assert paginator.current_page == 4

    with pytest.raises(ValueError):
        paginator.current_page = 99


def test_paginator_paging_start(paginator):
    assert paginator.has_next
    assert not paginator.has_previous
    assert paginator.previous_page_number == paginator._current_page
    assert paginator.next_page_number == paginator._current_page + 1
    assert paginator.num_pages == 9


def test_paginator_paging_alter(paginator):
    paginator.current_page = 6
    assert paginator.has_next
    assert paginator.has_previous
    assert paginator.previous_page_number == 5
    assert paginator.next_page_number == 7

    paginator.current_page = 9
    assert paginator.next_page_number == 9


def test_pagination_short():
    paginator = Paginator(sequence=ascii_uppercase,
                          current_page=1,
                          items_per_page=10)
    assert list(paginator) == [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'
    ]

    assert list(paginator.iterate_over_pages()) == [
        {'is_current': True, 'is_dummy': False, 'number': 1},
        {'is_current': False, 'is_dummy': False, 'number': 2},
        {'is_current': False, 'is_dummy': False, 'number': 3}
    ]


def test_pagination_long_1():
    paginator = Paginator(sequence=ascii_uppercase,
                          current_page=1,
                          items_per_page=3,
                          max_pages_in_block=2)
    assert list(paginator) == ['A', 'B', 'C']
    pages = [x['number'] for x in paginator.iterate_over_pages()]
    assert pages == [1, 2, -1, 3, 4, -1, 8, 9]


def test_pagination_long_2():
    paginator = Paginator(sequence=ascii_uppercase,
                          current_page=1,
                          items_per_page=3,
                          max_pages_in_block=3)
    assert list(paginator) == ['A', 'B', 'C']
    pages = [x['number'] for x in paginator.iterate_over_pages()]
    assert pages == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_pagination_long_3():
    paginator = Paginator(sequence=ascii_uppercase,
                          current_page=1,
                          items_per_page=2,
                          max_pages_in_block=3)
    assert list(paginator) == ['A', 'B']
    pages = [x['number'] for x in paginator.iterate_over_pages()]
    assert pages == [1, 2, 3, -1, 5, 6, 7, -1, 11, 12, 13]


def test_pagination_long_4():
    paginator = Paginator(sequence=ascii_uppercase * 40,
                          current_page=1,
                          items_per_page=10,
                          max_pages_in_block=4)
    assert len(list(paginator)) == 10
    pages = [x['number'] for x in paginator.iterate_over_pages()]
    assert pages == [1, 2, 3, 4, -1, 50, 51, 52, 53, -1, 101, 102, 103, 104]


def test_pagination_iter():
    paginator = Paginator(sequence=ascii_uppercase,
                          current_page=9,
                          items_per_page=3)

    assert list(paginator) == ['Y', 'Z']

    paginator.current_page = 2
    assert list(paginator) == ['D', 'E', 'F']

    paginator.current_page = 3
    assert list(paginator) == ['G', 'H', 'I']

    paginator.current_page = 9
    assert list(paginator) == ['Y', 'Z']

    paginator.current_page = 1
    assert list(paginator) == ['A', 'B', 'C']
