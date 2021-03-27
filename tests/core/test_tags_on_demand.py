# -*- coding: utf-8 -*-

"""Tests.
"""
import operator
from functools import partial, reduce

from mss.core.class_tags_on_demand import TagsOnDemand


def test_tags_on_demand_creation(tags_on_demand):
    assert str(tags_on_demand) == "TagsOnDemand(['a', 'b', 'c', 'd'])"


def test_tags_on_demand_iteration(tags_on_demand):
    assert set(tags_on_demand) == {'a', 'b', 'c', 'd'}


def test_tags_on_demand_from_dict():
    inst = TagsOnDemand.from_dict({
        'first comment': ['one', 'two'],
        'second_comment': ['three', 'four'],
        'third_comment': 'something',
    })
    assert list(inst) == ['four', 'one', 'something', 'three', 'two']


def test_tags_on_demand_contains(tags_on_demand):
    assert 'a' in tags_on_demand
    assert 'z' not in tags_on_demand


def test_tags_on_demand_sum():
    inst1 = TagsOnDemand(['a', 'b', 'c', 'd'])
    inst2 = TagsOnDemand(['c', 'd', 'e', 'f'])
    ref = TagsOnDemand(['a', 'b', 'c', 'd', 'e', 'f'])
    assert inst1 + inst2 == ref
    assert inst2 + inst1 == ref

    _sum = partial(reduce, operator.add)
    assert _sum([inst1, inst2]) == ref


def test_bool():
    inst1 = TagsOnDemand([])
    assert not inst1
    inst2 = TagsOnDemand(['a', 'b', 'c', 'd'])
    assert inst2
