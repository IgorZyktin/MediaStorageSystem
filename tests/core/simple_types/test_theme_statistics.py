# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from core.simple_types.class_theme_statistics import ThemeStatistics


@pytest.fixture
def statistics():
    inst = ThemeStatistics()
    inst.add_item('2021-10-01', 25, ['alpha', 'beta', 'gamma'])
    inst.add_item('2021-06-14', 250, ['alpha', 'cat', 'dog', 'fish'])
    inst.add_item('2021-02-28', 780, ['beta', 'home', 'ball', 'trust'])
    return inst


def test_statistics_creation(statistics):
    assert str(statistics) == 'ThemeStatistics<total_items=3>'


def test_statistics_as_dict(statistics):
    assert statistics.as_dict() == {}


def test_statistics_tags_by_popularity(statistics):
    assert statistics.tags_by_popularity == {
        'alpha': 2,
        'ball': 2,
        'beta': 1,
        'cat': 1,
        'dog': 1,
        'fish': 1,
        'gamma': 1,
        'home': 1,
        'trust': 1,
    }


def test_statistics_tags_by_alphabet(statistics):
    assert statistics.tags_by_alphabet == {
        'A': ['alpha'],
        'B': ['ball', 'beta'],
        'C': ['cat'],
        'D': ['dog'],
        'F': ['fish'],
        'G': ['gamma'],
        'H': ['home'],
        'T': ['trust'],
    }
