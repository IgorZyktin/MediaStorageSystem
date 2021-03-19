# -*- coding: utf-8 -*-

"""Tests.
"""
from mss.core.simple_types.class_serializer import Serializer
from mss.core.concrete_types.class_meta import Meta


class Demo:
    """Test class.
    """
    x: int
    y: str
    z: list

    def __init__(self, x, y, z):
        """Initialize instance."""
        self.x = x
        self.y = y
        self.z = z


def test_serializer_to_dict():
    inst1 = Demo(x=25, y='string', z=[1, 2, 3])
    inst2 = Demo(x=14, y='lol', z=[])

    serializer = Serializer(Demo)

    assert serializer.serialize(inst1) == {
        'x': 25,
        'y': 'string',
        'z': [1, 2, 3],
    }
    assert serializer.serialize(inst2) == {
        'x': 14,
        'y': 'lol',
        'z': [],
    }


def test_serializer_from_dict():
    serializer = Serializer(Demo)
    inst1 = serializer.from_source(**{
        'x': 25,
        'y': 'string',
        'z': [1, 2, 3],
    })
    assert inst1.x == 25
    assert inst1.y == 'string'
    assert inst1.z == [1, 2, 3]

    inst2 = serializer.from_source(**{
        'x': 14,
        'y': 'lol',
        'z': [],
    })
    assert inst2.x == 14
    assert inst2.y == 'lol'
    assert inst2.z == []


def test_serializer_to_dict_missed_attrs():
    inst1 = Demo(x=25, y='string', z=[1, 2, 3])
    inst2 = Demo(x=14, y='lol', z=[])

    del inst1.y
    del inst1.z
    del inst2.x
    del inst2.z

    serializer = Serializer(Demo)

    ser1 = serializer.serialize(inst1)
    assert ser1 == {
        'x': 25,
        'y': '',
        'z': [],
    }
    ser2 = serializer.serialize(inst2)
    assert ser2 == {
        'x': 0,
        'y': 'lol',
        'z': [],
    }
    assert ser1['z'] is not ser2['z']


def test_serializer_from_dict_missed_attrs():
    serializer = Serializer(Demo)
    inst1 = serializer.from_source(**{
        'x': 25,
        'y': 'string',
    })
    assert inst1.x == 25
    assert inst1.y == 'string'
    assert inst1.z == []

    inst2 = serializer.from_source(**{
        'x': 14,
    })
    assert inst2.x == 14
    assert inst2.y == ''
    assert inst2.z == []

    assert inst1.z is not inst2.z


def test_meta_from_source(valid_metarecord_dict):
    serializer = Serializer(Meta)
    instance = serializer.from_source(**valid_metarecord_dict)
    assert instance.media_type == valid_metarecord_dict['media_type']


def test_meta_serialize(valid_metarecord_dict):
    serializer = Serializer(Meta)
    instance = serializer.from_source(**valid_metarecord_dict)
    serialized = serializer.serialize(instance)
    assert valid_metarecord_dict == serialized


def test_meta_creation_from_nothing(valid_empty_metarecord):
    serializer = Serializer(Meta)
    instance = serializer.from_source()
    serialized = serializer.serialize(instance)
    assert valid_empty_metarecord == serialized


def test_meta_serialization_from_incorrect_format(valid_metarecord_dict):
    serializer = Serializer(Meta)
    instance = serializer.from_source(**valid_metarecord_dict)
    del instance.uuid
    del instance.media_type
    serialized = serializer.serialize(instance)

    corrupted_dict = valid_metarecord_dict.copy()
    corrupted_dict['uuid'] = ''
    corrupted_dict['media_type'] = ''
    assert corrupted_dict == serialized
