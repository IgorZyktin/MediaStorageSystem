# -*- coding: utf-8 -*-

"""Tests.
"""
from mss.core.simple_types.class_tags_on_demand import TagsOnDemand


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
