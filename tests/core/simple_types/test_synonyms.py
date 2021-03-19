# -*- coding: utf-8 -*-

"""Tests.
"""
from mss.core.simple_types.class_synonyms import Synonyms


def test_synonyms_creation(synonyms):
    assert str(synonyms) == 'Synonyms<2 groups>'


def test_synonyms_iteration(synonyms):
    assert list(synonyms) == [frozenset({'b', 'a'}),
                              frozenset({'d', 'c'})]


def test_synonyms_from_dict():
    inst = Synonyms.from_dict({
        'first comment': ['one', 'two'],
        'second_comment': ['three', 'four'],
    })
    assert list(inst) == [frozenset({'one', 'two'}),
                          frozenset({'three', 'four'})]
