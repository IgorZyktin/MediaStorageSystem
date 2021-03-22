# -*- coding: utf-8 -*-

"""Tests.
"""


def test_query_creation(query, empty_query):
    assert query
    assert not empty_query


def test_query_attrs(query):
    assert 'and_this' in query.and_


def test_as_dict(query, empty_query):
    assert query.as_dict() == {
        'and_': ['and_that', 'and_this'],
        'or_': ['or_that', 'or_this'],
        'not_': ['not_this'],
        'include': ['only this'],
        'exclude': ['except_this'],
        'flags': [],
    }

    assert empty_query.as_dict() == {
        'and_': [],
        'or_': [],
        'not_': ['not_this'],
        'include': ['only this'],
        'exclude': ['except_this'],
        'flags': [],
    }


def test_query_str(query, empty_query):
    assert str(query) == ('AND and_that '
                          'AND and_this '
                          'OR or_that '
                          'OR or_this '
                          'NOT not_this '
                          'INCLUDE only this '
                          'EXCLUDE except_this')

    assert str(empty_query) == ('NOT not_this '
                                'INCLUDE only this '
                                'EXCLUDE except_this')
