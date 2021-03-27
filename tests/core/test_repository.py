# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from mss.core import Repository, Meta


@pytest.fixture
def valid_metarecord(valid_metarecord_dict):
    return Meta(**valid_metarecord_dict)


def test_create_repository():
    inst = Repository()
    assert len(inst) == 0
    assert 'wtf' not in inst
    assert str(inst) == 'Repository<len=0>'


def test_add_record(valid_metarecord):
    inst = Repository()
    assert len(inst) == 0
    inst.add(valid_metarecord)

    assert len(inst) == 1
    assert str(inst) == 'Repository<len=1>'
    assert valid_metarecord.uuid in inst


def test_add_record_twice(valid_metarecord):
    inst = Repository()
    inst.add(valid_metarecord)

    msg = "Record Meta<uuid='008a2494-a6a4-4d63-886d-9e050f7a0d4a', " \
          "'original_filename.jpg'> is already in repository"

    with pytest.raises(ValueError, match=msg):
        inst.add(valid_metarecord)


def test_get_record(valid_metarecord):
    inst = Repository()
    inst.add(valid_metarecord)
    returned = inst.get_record(valid_metarecord.uuid)
    assert returned is valid_metarecord


def test_delete_record(valid_metarecord):
    inst = Repository()
    inst.add(valid_metarecord, {'something'})

    assert valid_metarecord.uuid in inst

    assert inst.get_extended_tags(valid_metarecord.uuid) \
           == {'something'} | set(valid_metarecord.tags)
    assert inst.get_uuids_by_tag('tag1') == {valid_metarecord.uuid}
    inst.delete_record(valid_metarecord.uuid)
    assert valid_metarecord.uuid not in inst

    assert inst.get_extended_tags(valid_metarecord.uuid) == set()
    assert inst.get_uuids_by_tag('tag1') == set()

    assert inst.delete_record('wtf') is None


def test_iter(valid_metarecord):
    inst = Repository()
    inst.add(valid_metarecord)
    assert list(iter(inst)) == [(valid_metarecord.uuid, valid_metarecord)]


def test_all_uuids(valid_metarecord):
    inst = Repository()
    inst.add(valid_metarecord)
    assert list(inst.all_uuids()) == [valid_metarecord.uuid]


def test_all_records(valid_metarecord):
    inst = Repository()
    inst.add(valid_metarecord)
    assert list(inst.all_records()) == [valid_metarecord]


def test_all_items(valid_metarecord):
    inst = Repository()
    inst.add(valid_metarecord)
    assert list(inst.all_items()) == [
        (valid_metarecord.uuid, valid_metarecord)]


def test_clear(valid_metarecord):
    inst = Repository()
    inst.add(valid_metarecord)
    assert inst.get_extended_tags(valid_metarecord.uuid)
    assert inst.get_uuids_by_tag(valid_metarecord.tags[0])
    assert len(inst)

    inst.clear()
    assert not inst.get_extended_tags(valid_metarecord.uuid)
    assert not inst.get_uuids_by_tag(valid_metarecord.tags[0])
    assert not len(inst)
