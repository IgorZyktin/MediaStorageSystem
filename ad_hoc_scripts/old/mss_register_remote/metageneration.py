# -*- coding: utf-8 -*-

"""Simplified metainfo construction.
"""


def make_base_metainfo() -> dict:
    """Return generic metainfo.
    """
    return {
        'uuid': '',

        'path_to_content': '',
        'path_to_preview': '',
        'path_to_thumbnail': '',

        'original_filename': '',
        'original_name': '',
        'original_extension': '',

        'series': '',
        'sub_series': '',
        'ordering': -1,
        'next_record': '',
        'previous_record': '',
        'group_name': '',
        'group_members': [],

        'width': 0,
        'height': 0,
        'resolution': 0.0,
        'media_type': '',
        'bytes_in_file': 0,
        'seconds': 0,

        'registered_on': '',
        'registered_by_username': '',
        'registered_by_nickname': '',

        'author': '',
        'author_url': '',
        'origin_url': '',
        'comment': '',

        'signature': '',
        'signature_type': '',

        'tags': []
    }


def make_metainfo_from_kw(**kwargs) -> dict:
    """Return basic metainfo + added keywords.
    """
    return {
        **make_base_metainfo(),
        **kwargs,
    }
