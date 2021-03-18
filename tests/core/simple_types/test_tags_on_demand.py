# -*- coding: utf-8 -*-

"""Tests.
"""
from core.simple_types.class_tags_on_demand import TagsOnDemand


def test_tags_on_demand_creation():
    inst = TagsOnDemand(['a', 'b', 'c', 'd'])
    assert str(inst) == "TagsOnDemand(['a', 'b', 'c', 'd'])"


def test_tags_on_demand_iteration():
    inst = TagsOnDemand(['a', 'b', 'c', 'd'])
    assert set(inst) == {'a', 'b', 'c', 'd'}


def test_tags_on_demand_from_dict():
    inst = TagsOnDemand.from_dict({
        'first comment': ['one', 'two'],
        'second_comment': ['three', 'four'],
        'third_comment': 'something',
    })
    assert list(inst) == ['four', 'one', 'something', 'three', 'two']


def test_tags_on_demand_contains():
    inst = TagsOnDemand(['a', 'b', 'c'])
    assert 'a' in inst
    assert 'z' not in inst
