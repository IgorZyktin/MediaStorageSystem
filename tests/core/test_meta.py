# -*- coding: utf-8 -*-

"""Tests.
"""

from mss.core import Meta


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
