# -*- coding: utf-8 -*-

"""Tests.
"""
from core.simple_types.class_synonyms import Synonyms


def test_synonyms_creation():
    inst = Synonyms([['a', 'b'], ['c', 'd']])
    assert str(inst) == 'Synonyms<2 groups>'


def test_synonyms_iteration():
    inst = Synonyms([['a', 'b'], ['c', 'd']])
    assert list(inst) == [frozenset({'b', 'a'}),
                          frozenset({'d', 'c'})]


def test_synonyms_from_dict():
    inst = Synonyms.from_dict({
        'first comment': ['one', 'two'],
        'second_comment': ['three', 'four'],
    })
    assert list(inst) == [frozenset({'one', 'two'}),
                          frozenset({'three', 'four'})]
