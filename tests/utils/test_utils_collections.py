# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from mss.utils.utils_collections import arrange_by_alphabet, group_to_size


@pytest.fixture
def input_data_arrange():
    return [
        '#',
        'acquire',
        'acquire',
        'constrain',
        'enthusiastic',
        'think',
        'edge',
    ]


@pytest.fixture
def ref_data_arrange_duplicates():
    return {
        '#': ['#'],
        'A': ['acquire', 'acquire'],
        'C': ['constrain'],
        'E': ['edge', 'enthusiastic'],
        'T': ['think'],
    }


@pytest.fixture
def ref_data_arrange_unique():
    return {
        '#': ['#'],
        'A': ['acquire'],
        'C': ['constrain'],
        'E': ['edge', 'enthusiastic'],
        'T': ['think'],
    }


def test_arrange_by_alphabet(input_data_arrange, ref_data_arrange_duplicates):
    """Must arrange by alphabet, no duplicate deletion."""
    assert arrange_by_alphabet(input_data_arrange,
                               unique=False) == ref_data_arrange_duplicates


def test_arrange_by_alphabet_unique(input_data_arrange,
                                    ref_data_arrange_unique):
    """Must arrange by alphabet with duplicate deletion."""
    assert arrange_by_alphabet(input_data_arrange,
                               unique=True) == ref_data_arrange_unique


def test_group_to_size():
    """Must form sized sequences."""
    res = list(group_to_size([1, 2, 3, 4, 5, 6, 7], 2, '?'))
    assert res == [(1, 2), (3, 4), (5, 6), (7, '?')]

    res = list(group_to_size([1, 2, 3, 4, 5, 6, 7], 3, '?'))
    assert res == [(1, 2, 3), (4, 5, 6), (7, '?', '?')]
