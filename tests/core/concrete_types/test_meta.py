# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from mss.core.abstract_types.class_abstract_meta import AbstractMeta
from mss.core.concrete_types.class_meta import Meta


@pytest.fixture
def invalid_metarecord():
    return {
        'uuid': '1'
    }


@pytest.fixture
def invalid_metarecord_field_diff():
    return list(AbstractMeta.__annotations__.keys())[1:]


def test_metarecord_creation_failed_kwargs(invalid_metarecord,
                                           invalid_metarecord_field_diff):
    msg = ('Meta instance has unmatched attributes: '
           + ', '.join(invalid_metarecord_field_diff))
    with pytest.raises(AttributeError, match=msg):
        Meta(**invalid_metarecord)


def test_metarecord_creation_correct(valid_metarecord_dict):
    instance = Meta(**valid_metarecord_dict)
    assert instance.uuid == valid_metarecord_dict['uuid']
    assert instance.original_name == valid_metarecord_dict['original_name']
    assert instance.media_type == valid_metarecord_dict['media_type']


def test_metarecord_repr(valid_metarecord_dict):
    instance = Meta(**valid_metarecord_dict)
    assert str(instance) == "Meta<uuid='008a2494-a6a4-4d63-886d-" \
                            "9e050f7a0d4a', 'original_filename.jpg'>"


def test_meta_ordering(valid_metarecord_dict):
    meta_1 = Meta(**{**valid_metarecord_dict, **dict(series='a',
                                                     sub_series='a',
                                                     ordering=3)})
    meta_2 = Meta(**{**valid_metarecord_dict, **dict(series='a',
                                                     sub_series='a',
                                                     ordering=2)})
    meta_3 = Meta(**{**valid_metarecord_dict, **dict(series='a',
                                                     sub_series='a',
                                                     ordering=1)})
    metas = [meta_1, meta_2, meta_3]
    metas.sort()
    assert metas == [meta_3, meta_2, meta_1]
