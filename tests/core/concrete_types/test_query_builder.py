# -*- coding: utf-8 -*-

"""Tests.
"""
from mss import constants


def test_query_builder_1(query_builder):
    text = 'cats OR dogs'
    directory = constants.ALL_THEMES
    query = query_builder.from_query(text, directory)
    assert query.as_dict() == {
        'and_': [],
        'or_': ['cats', 'dogs'],
        'not_': [],
        'include': [],
        'exclude': [],
        'flags': [],
    }
    assert str(query) == 'OR cats OR dogs'


def test_query_builder_2(query_builder):
    text = 'AND cats OR dogs AND turtle NOT frog AND IMAGE INCLUDE test'
    directory = constants.ALL_THEMES
    query = query_builder.from_query(text, directory)
    assert query.as_dict() == {
        'and_': [constants.TYPE_IMAGE, 'cats', 'turtle'],
        'or_': ['dogs'],
        'not_': ['frog'],
        'include': ['test'],
        'exclude': [],
        'flags': [],
    }
    assert str(query) == ('AND IMAGE '
                          'AND cats '
                          'AND turtle '
                          'OR dogs '
                          'NOT frog '
                          'INCLUDE test')


def test_query_builder_3(query_builder):
    text = 'OR fly AND fish EXCLUDE spiders OR HUGE OR AUDIO'
    directory = 'somewhere'
    query = query_builder.from_query(text, directory)
    assert query.as_dict() == {
        'and_': [constants.TYPE_AUDIO, constants.RES_HUGE, 'fish'],
        'or_': ['fly'],
        'not_': [],
        'include': ['somewhere'],
        'exclude': ['spiders'],
        'flags': [],
    }
    assert str(query) == ('AND AUDIO '
                          'AND HUGE '
                          'AND fish '
                          'OR fly '
                          'INCLUDE somewhere '
                          'EXCLUDE spiders')


def test_query_builder_wrong_1(query_builder, bad_query_dict):
    text = 'cats AND NOT dogs'
    directory = constants.ALL_THEMES
    query = query_builder.from_query(text, directory)
    assert query.as_dict() == bad_query_dict
    assert str(query) == 'AND ' + constants.NEVER_FIND_THIS + ' OR cats'


def test_query_builder_empty(query_builder, empty_query_dict):
    text = ''
    directory = constants.ALL_THEMES
    query = query_builder.from_query(text, directory)
    assert query.as_dict() == empty_query_dict
    assert str(query) == ''


def test_query_builder_flags(query_builder, empty_query_dict):
    text = 'AND some AND other NOT DEMAND NOT DESC'
    directory = constants.ALL_THEMES
    query = query_builder.from_query(text, directory)
    assert query.as_dict() == {
        'and_': ['other', 'some'],
        'or_': [],
        'not_': [],
        'include': [],
        'flags': [constants.FLAG_DEMAND, constants.FLAG_DESC],
        'exclude': [],
    }
    assert str(query) == 'AND other AND some AND DEMAND AND DESC'
