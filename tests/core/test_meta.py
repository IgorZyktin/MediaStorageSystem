# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from core.class_imeta import IMeta
from core.class_meta import Meta


@pytest.fixture
def invalid_metarecord():
    return {
        'uuid': '1'
    }


@pytest.fixture
def invalid_metarecord_field_diff():
    return list(IMeta.__annotations__.keys())[1:]


def test_metarecord_creation_failed_args():
    msg = 'Meta does not take positional arguments'
    with pytest.raises(ValueError, match=msg):
        Meta(1, 2, 3)


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
