# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from mss import constants
from mss.core.concrete_types.class_query_builder import QueryBuilder
from mss.core.simple_types.class_query import Query


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
