# -*- coding: utf-8 -*-

"""Tests.
"""
from unittest.mock import ANY


def test_statistics_creation(statistics):
    assert str(statistics) == 'ThemeStatistics<total_items=3>'


def test_statistics_as_dict(statistics):
    assert statistics.as_dict() == {
        'Newest item': '2021-10-01',
        'Oldest item': '2021-02-28',
        'Total items': '3',
        'Total size': '1.0 KiB',
        'Total tags': '9',
        'tags_by_alphabet': ANY,
        'tags_by_popularity': ANY
    }


def test_statistics_tags_by_popularity(statistics):
    assert statistics.tags_by_popularity == [
        ('alpha', 2),
        ('beta', 2),
        ('ball', 1),
        ('cat', 1),
        ('dog', 1),
        ('fish', 1),
        ('gamma', 1),
        ('home', 1),
        ('trust', 1),
    ]


def test_statistics_tags_by_alphabet(statistics):
    assert statistics.tags_by_alphabet == [
        ('A', ['alpha']),
        ('B', ['ball', 'beta']),
        ('C', ['cat']),
        ('D', ['dog']),
        ('F', ['fish']),
        ('G', ['gamma']),
        ('H', ['home']),
        ('T', ['trust']),
    ]


def test_statistics_iteration(statistics):
    assert list(statistics) == [
        ('Total items', '3'),
        ('Total size', '1.0 KiB'),
        ('Oldest item', '2021-02-28'),
        ('Newest item', '2021-10-01'),
        ('Total tags', '9'),
    ]


def test_statistics_sum(statistics):
    assert statistics.as_dict() == {
        'Newest item': '2021-10-01',
        'Oldest item': '2021-02-28',
        'Total items': '3',
        'Total size': '1.0 KiB',
        'Total tags': '9',
        'tags_by_alphabet': [('A', ['alpha']),
                             ('B', ['ball', 'beta']),
                             ('C', ['cat']),
                             ('D', ['dog']),
                             ('F', ['fish']),
                             ('G', ['gamma']),
                             ('H', ['home']),
                             ('T', ['trust'])],
        'tags_by_popularity': [('alpha', 2),
                               ('beta', 2),
                               ('ball', 1),
                               ('cat', 1),
                               ('dog', 1),
                               ('fish', 1),
                               ('gamma', 1),
                               ('home', 1),
                               ('trust', 1)]
    }

    assert (statistics + statistics + statistics).as_dict() == {
        'Newest item': '2021-10-01',
        'Oldest item': '2021-02-28',
        'Total items': '9',
        'Total size': '3.1 KiB',
        'Total tags': '9',
        'tags_by_alphabet': [('A', ['alpha']),
                             ('B', ['ball', 'beta']),
                             ('C', ['cat']),
                             ('D', ['dog']),
                             ('F', ['fish']),
                             ('G', ['gamma']),
                             ('H', ['home']),
                             ('T', ['trust'])],
        'tags_by_popularity': [('alpha', 6),
                               ('beta', 6),
                               ('ball', 3),
                               ('cat', 3),
                               ('dog', 3),
                               ('fish', 3),
                               ('gamma', 3),
                               ('home', 3),
                               ('trust', 3)],
    }
