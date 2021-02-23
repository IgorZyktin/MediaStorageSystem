# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from browser.utils_browser import extend_tags_with_synonyms


@pytest.fixture
def ref_tags():
    return {'__another_testing', '__testing'}


def test_synonyms_empty():
    tags = set()
    extend_tags_with_synonyms(tags)
    assert tags == set()


def test_synonyms_present_1(ref_tags):
    tags = {'__testing'}
    extend_tags_with_synonyms(tags)
    assert tags == ref_tags


def test_synonyms_present_2(ref_tags):
    tags = {'__another_testing'}
    extend_tags_with_synonyms(tags)
    assert tags == ref_tags
