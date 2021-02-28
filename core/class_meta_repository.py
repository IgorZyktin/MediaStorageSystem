# -*- coding: utf-8 -*-

"""Storage for metarecords.
"""
from typing import Dict, Optional

from core.class_imeta import IMeta


class MetaRepository:
    """Storage for metarecords.
    """

    def __init__(self, *args: IMeta) -> None:
        """Initialize instance.
        """
        self._storage: Dict[str, IMeta] = {}

        for arg in args:
            self.add_record(arg)

    def __contains__(self, item: str) -> bool:
        """Return True if uuid is in our storage.
        """
        return item in self._storage

    def __repr__(self) -> str:
        """Return textual representation.
        """
        return f'{type(self).__name__}<records={len(self._storage)}>'

    def __len__(self) -> int:
        """Return amount of records inside repository.
        """
        return len(self._storage)

    def __iter__(self):
        """Iterate on records.
        """
        return iter(self._storage.values())

    def add_record(self, new_record: IMeta) -> None:
        """Add record to repository.
        """
        if new_record.uuid in self._storage:
            raise ValueError(f'Record {new_record} is already in repository')

        self._storage[new_record.uuid] = new_record

    def drop_record(self, uuid: str) -> Optional[IMeta]:
        """Return instance if present and delete it from storage.
        """
        instance = self._storage.pop(uuid, None)

        if instance is None:
            return instance

    def get(self, uuid: str) -> Optional[IMeta]:
        """Return record or None if not present.
        """
        return self._storage.get(uuid)

    def clear(self) -> None:
        """Drop all records.
        """
        self._storage.clear()
