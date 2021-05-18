# -*- coding: utf-8 -*-

"""Tests.
"""
import random

from mss import core, constants
from _demo.search.class_search_enhancer import (
    get_duration_tag,
    get_image_size_tag,
)


def test_search_enhancer_get_extended_tags():
    synonyms = core.Synonyms([['red', 'green'], ['blue', 'brown']])
    enhancer = core.SearchEnhancer(synonyms)
    meta = core.Meta(tags=['red'])

    assert enhancer.get_extended_tags(meta) == {
        '',
        'red',
        'UNKNOWN',
    }

    assert enhancer.get_extended_tags_with_synonyms(meta) == {
        '',
        'red',
        'green',
        'UNKNOWN',
    }


def test_get_image_size_tag():
    tiny = random.randint(
        1,
        int(constants.THRESHOLD_TINY * 1000) - 1
    ) / 1000
    assert get_image_size_tag(tiny) == constants.RES_TINY

    small = random.randint(
        int(constants.THRESHOLD_TINY * 1000),
        int(constants.THRESHOLD_SMALL * 1000) - 1
    ) / 1000
    assert get_image_size_tag(small) == constants.RES_SMALL

    mean = random.randint(
        int(constants.THRESHOLD_SMALL * 1000),
        int(constants.THRESHOLD_MEAN * 1000) - 1
    ) / 1000
    assert get_image_size_tag(mean) == constants.RES_MEAN

    big = random.randint(
        int(constants.THRESHOLD_MEAN * 1000),
        int(constants.THRESHOLD_BIG * 1000) - 1
    ) / 1000
    assert get_image_size_tag(big) == constants.RES_BIG

    huge = random.randint(
        int(constants.THRESHOLD_BIG * 1000),
        int(constants.THRESHOLD_BIG * 1000) + 1
    ) / 1000
    assert get_image_size_tag(huge) == constants.RES_HUGE


def test_get_duration_tag():
    moment = random.randint(
        1,
        int(constants.THRESHOLD_MOMENT) - 1
    )
    assert get_duration_tag(moment) == constants.DUR_MOMENT

    short = random.randint(
        int(constants.THRESHOLD_MOMENT),
        int(constants.THRESHOLD_SHORT) - 1
    )
    assert get_duration_tag(short) == constants.DUR_SHORT

    medium = random.randint(
        int(constants.THRESHOLD_SHORT),
        int(constants.THRESHOLD_MEDIUM) - 1
    )
    assert get_duration_tag(medium) == constants.DUR_MEDIUM

    long = random.randint(
        int(constants.THRESHOLD_MEDIUM),
        int(constants.THRESHOLD_MEDIUM) + 1
    )
    assert get_duration_tag(long) == constants.DUR_LONG
