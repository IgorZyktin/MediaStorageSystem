# -*- coding: utf-8 -*-

"""Storage for metarecords.
"""
from collections import defaultdict
from typing import Dict, Optional, Set, ItemsView, KeysView, ValuesView

from mss.core.class_meta import Meta


class Repository:
    """Storage for metarecords.
    """

    def __init__(self) -> None:
        """Initialize instance."""
        self._storage_of_records: Dict[str, Meta] = {}
        self._uuid_by_tag: Dict[str, Set[str]] = defaultdict(set)
        self._extended_tags_for_records: Dict[str, Set[str]] = {}

    def __contains__(self, uuid: str) -> bool:
        """Return True if uuid is in our storage.
        """
        return uuid in self._storage_of_records

    def __repr__(self) -> str:
        """Return textual representation.
        """
        return f'{type(self).__name__}<len={len(self._storage_of_records)}>'

    def __len__(self) -> int:
        """Return amount of records inside repository.
        """
        return len(self._storage_of_records)

    def __iter__(self) -> ItemsView[str, Meta]:
        """Iterate on records.
        """
        return iter(self.all_items())

    def add_record(self, new_record: Meta,
                   extended_tags: Optional[Set[str]] = None) -> None:
        """Add record into repository.

        :raises: ValueError if record already exist.
        """
        if new_record.uuid in self._storage_of_records:
            raise ValueError(f'Record {new_record} is already in repository')

        self._storage_of_records[new_record.uuid] = new_record

        if not extended_tags:
            extended_tags = set(new_record.tags)
        else:
            extended_tags = set(new_record.tags) | extended_tags

        self._extended_tags_for_records[new_record.uuid] = extended_tags

        for tag in extended_tags:
            self._uuid_by_tag[tag].add(new_record.uuid)

    def get_record(self, uuid: str) -> Optional[Meta]:
        """Return record or None if not present.
        """
        return self._storage_of_records.get(uuid)

    def delete_record(self, uuid: str) -> Optional[Meta]:
        """Return instance if present and delete it from storage.
        """
        instance = self._storage_of_records.pop(uuid, None)

        if instance is None:
            return None

        tags = self._extended_tags_for_records.get(uuid, set())
        for tag in tags:
            self._uuid_by_tag[tag].discard(uuid)

        self._extended_tags_for_records.pop(uuid)

        return instance

    def all_uuids(self) -> KeysView[str]:
        """Return UUIDs in the storage.
        """
        return self._storage_of_records.keys()

    def all_records(self) -> ValuesView[Meta]:
        """Return records in the storage.
        """
        return self._storage_of_records.values()

    def all_items(self) -> ItemsView[str, Meta]:
        """Return all uuid+record from the storage.
        """
        return self._storage_of_records.items()

    def get_uuids_by_tag(self, tag: str) -> Set[str]:
        """Return all UUIDs with this tag.
        """
        return self._uuid_by_tag.get(tag, set())

    def get_extended_tags(self, uuid: str) -> Set[str]:
        """Return extended tags for given record UUID.
        """
        return self._extended_tags_for_records.get(uuid, set())

    def clear(self) -> None:
        """Drop all records.
        """
        self._storage_of_records.clear()
        self._uuid_by_tag.clear()
        self._extended_tags_for_records.clear()
