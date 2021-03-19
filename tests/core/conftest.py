# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest


@pytest.fixture
def valid_metarecord_dict():
    return {
        'uuid': '008a2494-a6a4-4d63-886d-9e050f7a0d4a',
        'theme_directory': 'some_directory',

        'path_to_content': 'content',
        'path_to_preview': 'preview',
        'path_to_thumbnail': 'thumbnail',

        'original_filename': 'original_filename.jpg',
        'original_name': 'original_filename',
        'original_extension': 'jpg',
        'series': 'some series',
        'sub_series': 'some sub series',

        'group_name': 'some group',
        'group_members': ['a', 'b'],
        'previous_record': 'a',
        'next_record': 'b',
        'ordering': 132,

        'width': 1024,
        'height': 768,
        'resolution': 0.2,
        'bytes_in_file': 999,
        'seconds': 999,
        'media_type': 'static_image',

        'registered_on': '2021-02-20',
        'registered_by_username': 'Some Body',
        'registered_by_nickname': 'User',
        'author': 'some author',
        'author_url': 'some author profile',
        'origin_url': 'some page url',
        'comment': 'some comment',

        'signature': '123',
        'signature_type': 'random',

        'tags': ['tag1', 'tag2', 'tag3'],
    }


@pytest.fixture
def valid_empty_metarecord():
    return {
        'author': '',
        'author_url': '',
        'bytes_in_file': 0,
        'comment': '',
        'group_members': [],
        'group_name': '',
        'height': 0,
        'media_type': '',
        'next_record': '',
        'ordering': 0,
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
        'resolution': 0,
        'seconds': 0,
        'series': '',
        'signature': '',
        'signature_type': '',
        'sub_series': '',
        'tags': [],
        'uuid': '',
        'theme_directory': '',
        'width': 0,
    }
