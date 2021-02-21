# -*- coding: utf-8 -*-

"""Tests.
"""
from common.metarecord_helpers import *


def test_serializable():
    instance = Serializable()
    instance.x = 1
    instance.y = 'a'
    assert instance.to_dict() == {'x': 1, 'y': 'a'}


def test_content_info():
    instance = ContentInfo('path1', 'path2', 'path3')
    assert instance.to_dict() == {
        'content_path': 'path1',
        'preview_path': 'path2',
        'thumbnail_path': 'path3',
    }


def test_file_info():
    instance = FileInfo('txt', 'name', 'name.txt')
    assert instance.to_dict() == {
        'ext': 'txt',
        'original_filename': 'name.txt',
        'original_name': 'name',
    }


def test_meta():
    instance = Meta('video', 'show', 25, 'something')
    assert instance.to_dict() == {
        'comment': 'something',
        'ordering': 25,
        'series': 'video',
        'sub_series': 'show',
    }


def test_parameters():
    instance = Parameters(1024, 768, 0.25, 'image', 9999)
    assert instance.to_dict() == {
        'height': 768,
        'media_type': 'image',
        'resolution_mp': 0.25,
        'size': 9999,
        'width': 1024,
    }


def test_registration():
    instance = Registration('2021-02-20', 'test', 'user')
    assert instance.to_dict() == {
        'registered_at': '2021-02-20',
        'registered_by_nickname': 'user',
        'registered_by_username': 'test',
    }
