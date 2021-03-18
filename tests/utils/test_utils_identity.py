# -*- coding: utf-8 -*-

"""Tests.
"""
from itertools import cycle
from unittest.mock import patch

from mss.utils.utils_identity import get_new_uuid


def test_get_new_uuid():
    """Must generate UUID not in used range."""
    used_uuids = ['a', 'b', 'c']
    cycle_gen = cycle(used_uuids + ['d'])

    def func():
        return next(cycle_gen)

    with patch('mss.utils.utils_identity.uuid') as fake_uuid:
        fake_uuid.uuid4 = func
        set_used_uuids = set(used_uuids)
        assert get_new_uuid(set_used_uuids) not in used_uuids
