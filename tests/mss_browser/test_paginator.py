# -*- coding: utf-8 -*-

"""Tests.
"""
from string import ascii_uppercase

import pytest

from mss.mss_browser.class_paginator import Paginator


@pytest.fixture
def paginator():
    return Paginator(sequence=ascii_uppercase,
                     current_page=1,
                     items_per_page=3)


@pytest.fixture
def paginator_big():
    return Paginator(sequence=(ascii_uppercase * 40)[0:1000],
                     current_page=1,
                     items_per_page=10,
                     pages_in_block=5)


def _get_pages(paginator_inst):
    pages = []
    for page in paginator_inst.iterate_over_pages():
        if page['is_dummy']:
            pages.append('...')
        elif page['is_current']:
            pages.append('[' + str(page['number']) + ']')
        else:
            pages.append(str(page['number']))

    return pages


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


def test_pagination_long_1(paginator_big):
    paginator_big.current_page = 1
    pages = _get_pages(paginator_big)
    assert pages == ['[1]', '2', '3', '4', '5', '...', '100']


def test_pagination_long_2(paginator_big):
    paginator_big.current_page = 2
    pages = _get_pages(paginator_big)
    assert pages == ['1', '[2]', '3', '4', '5', '...', '100']


def test_pagination_long_3(paginator_big):
    paginator_big.current_page = 3
    pages = _get_pages(paginator_big)
    assert pages == ['1', '2', '[3]', '4', '5', '...', '100']


def test_pagination_long_4(paginator_big):
    paginator_big.current_page = 4
    pages = _get_pages(paginator_big)
    assert pages == ['1', '...', '2', '3', '[4]', '5', '6', '...', '100']


def test_pagination_long_5(paginator_big):
    paginator_big.current_page = 5
    pages = _get_pages(paginator_big)
    assert pages == ['1', '...', '3', '4', '[5]', '6', '7', '...', '100']


def test_pagination_long_6(paginator_big):
    paginator_big.current_page = 6
    pages = _get_pages(paginator_big)
    assert pages == ['1', '...', '4', '5', '[6]', '7', '8', '...', '100']


def test_pagination_long_7(paginator_big):
    paginator_big.current_page = 7
    pages = _get_pages(paginator_big)
    assert pages == ['1', '...', '5', '6', '[7]', '8', '9', '...', '100']


def test_pagination_long_8(paginator_big):
    paginator_big.current_page = 8
    pages = _get_pages(paginator_big)
    assert pages == ['1', '...', '6', '7', '[8]', '9', '10', '...', '100']


def test_pagination_long_95(paginator_big):
    paginator_big.current_page = 95
    pages = _get_pages(paginator_big)
    assert pages == ['1', '...', '93', '94', '[95]', '96', '97', '...', '100']


def test_pagination_long_96(paginator_big):
    paginator_big.current_page = 96
    pages = _get_pages(paginator_big)
    assert pages == ['1', '...', '94', '95', '[96]', '97', '98', '...', '100']


def test_pagination_long_97(paginator_big):
    paginator_big.current_page = 97
    pages = _get_pages(paginator_big)
    assert pages == ['1', '...', '95', '96', '[97]', '98', '99', '...', '100']


def test_pagination_long_98(paginator_big):
    paginator_big.current_page = 98
    pages = _get_pages(paginator_big)
    assert pages == ['1', '...', '96', '97', '[98]', '99', '100']


def test_pagination_long_99(paginator_big):
    paginator_big.current_page = 99
    pages = _get_pages(paginator_big)
    assert pages == ['1', '...', '96', '97', '98', '[99]', '100']


def test_pagination_long_100(paginator_big):
    paginator_big.current_page = 100
    pages = _get_pages(paginator_big)
    assert pages == ['1', '...', '96', '97', '98', '99', '[100]']
