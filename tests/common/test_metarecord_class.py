# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from common.metarecord_class import *


@pytest.fixture
def input_metarecord():
    return {
        "uuid": "008a2494-a6a4-4d63-886d-9e050f7a0d4a",
        "content_info": {
            "content_path": "content",
            "preview_path": "preview",
            "thumbnail_path": "thumbnail",
        },
        "file_info": {
            "original_filename": "original_filename.jpg",
            "original_name": "original_filename",
            "ext": "jpg",
        },
        "meta": {
            "series": "some series",
            "sub_series": "some sub series",
            "ordering": 132,
            "comment": "something",
        },
        "parameters": {
            "width": 1024,
            "height": 768,
            "resolution_mp": 0.2,
            "media_type": "static_image",
            "size": 999,
        },
        "registration": {
            "registered_at": "2021-02-20",
            "registered_by_username": "Some Body",
            "registered_by_nickname": "User",
        },
        "tags": ['__testing'],
    }


def test_metarecord_creation(input_metarecord):
    instance = Metarecord(**input_metarecord)
    assert str(instance) == ("Metarecord<uuid=008a2494-a6a4-4d63"
                             "-886d-9e050f7a0d4a, 'original_filename.jpg'>")
    assert instance.unique_filename == ('original_filename___008a2494-a6a4-'
                                        '4d63-886d-9e050f7a0d4a.jpg')


def test_metarecord_tags(input_metarecord):
    instance = Metarecord(**input_metarecord)
    assert instance.tags_set == {
        '__testing',
    }
    assert instance.extended_tags_set == {
        'some sub series',
        'some series',
        '__another_testing',
        '__testing',
    }


def test_metarecord_to_dict(input_metarecord):
    instance = Metarecord(**input_metarecord)
    assert instance.to_dict() == input_metarecord
