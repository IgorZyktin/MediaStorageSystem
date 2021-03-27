# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from mss import constants
from mss.core import (
    QueryBuilder, Query, ThemeStatistics, Synonyms,
    TagsOnDemand, Theme
)


@pytest.fixture
def valid_metarecord_dict():
    return {
        'uuid': '008a2494-a6a4-4d63-886d-9e050f7a0d4a',
        'directory': 'some_directory',

        'path_to_content': 'content',
        'path_to_preview': 'preview',
        'path_to_thumbnail': 'thumbnail',

        'original_filename': 'original_filename.jpg',
        'original_name': 'original_filename',
        'original_extension': 'jpg',
        'series': 'some series',
        'sub_series': 'some sub series',

        'group_name': 'some group',
        'group_members': ['a', 'b'],
        'previous_record': 'a',
        'next_record': 'b',
        'ordering': 132,

        'width': 1024,
        'height': 768,
        'resolution': 0.2,
        'bytes_in_file': 999,
        'seconds': 999,
        'media_type': 'static_image',

        'registered_on': '2021-02-20',
        'registered_by_username': 'Some Body',
        'registered_by_nickname': 'User',
        'author': 'some author',
        'author_url': 'some author profile',
        'origin_url': 'some page url',
        'comment': 'some comment',

        'signature': '123',
        'signature_type': 'random',

        'tags': ['tag1', 'tag2', 'tag3'],
    }


@pytest.fixture
def query_builder():
    inst = QueryBuilder(Query)
    return inst


@pytest.fixture
def empty_query_dict():
    return {
        'and_': [],
        'or_': [],
        'not_': [],
        'include': [],
        'exclude': [],
        'flags': [],
    }


@pytest.fixture
def bad_query_dict():
    return {
        'and_': [constants.NEVER_FIND_THIS],
        'or_': ['cats'],
        'not_': [],
        'include': [],
        'exclude': [],
        'flags': [],
    }


@pytest.fixture
def statistics():
    inst = ThemeStatistics()
    inst.add('2021-10-01', 25, ['alpha', 'beta', 'gamma'])
    inst.add('2021-06-14', 250, ['alpha', 'cat', 'dog', 'fish'])
    inst.add('2021-02-28', 780, ['beta', 'home', 'ball', 'trust'])
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


@pytest.fixture
def query():
    inst = Query(
        and_=frozenset(['and_this', 'and_that']),
        or_=frozenset(['or_this', 'or_that']),
        not_=frozenset(['not_this']),
        include=frozenset(['only this']),
        exclude=frozenset(['except_this']),
        flags=frozenset(),
    )
    return inst


@pytest.fixture
def empty_query():
    inst = Query(
        and_=frozenset(),
        or_=frozenset(),
        not_=frozenset(['not_this']),
        include=frozenset(['only this']),
        exclude=frozenset(['except_this']),
        flags=frozenset(),
    )
    return inst
