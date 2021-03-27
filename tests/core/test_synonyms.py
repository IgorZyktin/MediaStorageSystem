# -*- coding: utf-8 -*-

"""Tests.
"""
import operator
from functools import partial, reduce

from mss.core.class_synonyms import Synonyms


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


def test_synonyms_sum():
    inst1 = Synonyms([['a', 'b'], ['c', 'd']])
    inst2 = Synonyms([['c', 'd'], ['e', 'f']])
    ref = Synonyms([['a', 'b'], ['c', 'd'], ['e', 'f']])
    assert inst1 + inst2 == ref
    assert inst2 + inst1 == ref

    _sum = partial(reduce, operator.add)
    assert _sum([inst1, inst2]) == ref
