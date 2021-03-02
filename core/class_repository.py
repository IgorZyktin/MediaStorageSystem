# -*- coding: utf-8 -*-

"""Storage for metarecords.
"""
from collections import defaultdict
from typing import Dict, Optional, Iterable, Set

from core.class_imeta import IMeta


class Repository:
    """Storage for metarecords.
    """

    def __init__(self) -> None:
        """Initialize instance.
        """
        self._storage: Dict[str, IMeta] = {}
        self._uuid_by_tag: Dict[str, Set[str]] = defaultdict(set)
        self._extended_tags: Dict[str, Set[str]] = {}

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

    def add_record(self, new_record: IMeta, extended_tags: Set[str]) -> None:
        """Add record to repository.
        """
        if new_record.uuid in self._storage:
            raise ValueError(f'Record {new_record} is already in repository')

        self._storage[new_record.uuid] = new_record
        self._extended_tags[new_record.uuid] = extended_tags

        for tag in extended_tags:
            self._uuid_by_tag[tag].add(new_record.uuid)

    def drop_record(self, uuid: str) -> Optional[IMeta]:
        """Return instance if present and delete it from storage.
        """
        instance = self._storage.pop(uuid, None)

        if instance is None:
            return None

        tags = self._extended_tags.get(uuid, set())
        for tag in tags:
            self._uuid_by_tag[tag].discard(uuid)

        self._extended_tags.pop(uuid)

        return instance

    def keys(self) -> Iterable[str]:
        """Return UUIDs in the storage.
        """
        return self._storage.keys()

    def get(self, uuid: str) -> Optional[IMeta]:
        """Return record or None if not present.
        """
        return self._storage.get(uuid)

    def get_uuids_by_tag(self, uuid: str) -> Set[str]:
        """Return all UUIDs with this tag.
        """
        return self._uuid_by_tag.get(uuid, set())

    def clear(self) -> None:
        """Drop all records.
        """
        self._storage.clear()
