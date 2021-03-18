# -*- coding: utf-8 -*-

"""Special utils created to work with identification.
"""
import uuid
from typing import Set


def get_new_uuid(existing_uuids: Set[str]) -> str:
    """Generate new unique UUID."""
    new_uuid = str(uuid.uuid4())

    while new_uuid in existing_uuids:
        new_uuid = str(uuid.uuid4())

    return new_uuid
