# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from mss.core.simple_types.class_synonyms import Synonyms
from mss.core.simple_types.class_tags_on_demand import TagsOnDemand
from mss.core.simple_types.class_theme import Theme
from mss.core.simple_types.class_theme_statistics import ThemeStatistics


@pytest.fixture
def statistics():
    inst = ThemeStatistics()
    inst.add_item('2021-10-01', 25, ['alpha', 'beta', 'gamma'])
    inst.add_item('2021-06-14', 250, ['alpha', 'cat', 'dog', 'fish'])
    inst.add_item('2021-02-28', 780, ['beta', 'home', 'ball', 'trust'])
    return inst


@pytest.fixture
def synonyms():
    inst = Synonyms([['a', 'b'], ['c', 'd']])
    return inst


@pytest.fixture
def tags_on_demand():
    inst = TagsOnDemand(['a', 'b', 'c', 'd'])
    return inst


@pytest.fixture
def theme(statistics, synonyms, tags_on_demand):
    inst = Theme(
        name='Testing theme',
        directory='test_dir',
        synonyms=synonyms,
        tags_on_demand=tags_on_demand,
        statistics=statistics,
        used_uuids={'a', 'b', 'c'},
    )
    return inst


@pytest.fixture
def theme_another(statistics, synonyms, tags_on_demand):
    inst = Theme(
        name='Another theme',
        directory='test_another',
        synonyms=synonyms,
        tags_on_demand=tags_on_demand,
        statistics=statistics,
        used_uuids={'a', 'b', 'c'},
    )
    return inst
