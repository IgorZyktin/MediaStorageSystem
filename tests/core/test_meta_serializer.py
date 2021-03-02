# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from core.class_meta import Meta
from core.class_serializer import DictSerializer


@pytest.fixture
def serializer():
    return DictSerializer(Meta)


@pytest.fixture
def empty_instance():
    return {
        'author': '',
        'author_url': '',
        'bytes_in_file': -1,
        'comment': '',
        'group_members': [],
        'group_name': '',
        'height': -1,
        'media_type': '',
        'next_record': '',
        'ordering': -1,
        'origin_url': '',
        'original_extension': '',
        'original_filename': '',
        'original_name': '',
        'path_to_content': '',
        'path_to_preview': '',
        'path_to_thumbnail': '',
        'previous_record': '',
        'registered_by_nickname': '',
        'registered_by_username': '',
        'registered_on': '',
        'resolution': -1,
        'seconds': -1,
        'series': '',
        'signature': '',
        'signature_type': '',
        'sub_series': '',
        'tags': [],
        'uuid': '',
        'width': -1,
    }


def test_from_source(serializer, valid_metarecord_dict):
    instance = serializer.from_source(**valid_metarecord_dict)
    assert instance.media_type == valid_metarecord_dict['media_type']


def test_serialize(serializer, valid_metarecord_dict):
    instance = serializer.from_source(**valid_metarecord_dict)
    serialized = serializer.serialize(instance)
    assert valid_metarecord_dict == serialized


def test_creation_from_nothing(serializer, empty_instance):
    instance = serializer.from_source()
    serialized = serializer.serialize(instance)
    assert empty_instance == serialized


def test_serialization_from_incorrect_format(serializer,
                                             valid_metarecord_dict):
    instance = serializer.from_source(**valid_metarecord_dict)
    del instance.uuid
    del instance.media_type
    serialized = serializer.serialize(instance)

    corrupted_dict = valid_metarecord_dict.copy()
    corrupted_dict['uuid'] = ''
    corrupted_dict['media_type'] = ''
    assert corrupted_dict == serialized
