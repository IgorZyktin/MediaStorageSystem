# -*- coding: utf-8 -*-

"""Storage for metarecords.
"""
from typing import Dict, Any, Set, Optional

from core.class_imeta import IMeta


class MetaRepository:
    """Storage for metarecords.
    """

    def __init__(self, *args: IMeta) -> None:
        """Initialize instance.
        """
        self._storage: Dict[str, IMeta] = {}
        self._statistics: Dict[str, Any] = {}
        self._known_tags: Set[str] = set()

        self.clear_statistics()

        for arg in args:
            self.add_record(arg)

    def __repr__(self) -> str:
        """Return textual representation.
        """
        return f'{type(self).__name__}<records={len(self._storage)}>'

    def __len__(self) -> int:
        """Return amount of records inside repository.
        """
        return self._statistics.get('total_items', 0)

    def clear_statistics(self) -> None:
        """Restore statistics to the default.
        """
        self._statistics = {
            'total_items': 0,
            'total_size': 0,
            'min_date': '2040-01-01',
            'max_date': '1980-01-01',
        }

    def add_record(self, new_record: IMeta) -> None:
        """Add record to repository.
        """
        if new_record.uuid in self._storage:
            raise ValueError(f'Record {new_record} is already in repository')

        self._storage[new_record.uuid] = new_record
        self._known_tags.update(new_record.tags)

        self._statistics['total_items'] += 1
        self._statistics['total_size'] += new_record.bytes_in_file

        self._statistics['min_date'] = min(new_record.registered_at,
                                           self._statistics['min_date'])
        self._statistics['max_date'] = max(new_record.registered_at,
                                           self._statistics['max_date'])

    def drop_record(self, uuid: str) -> Optional[IMeta]:
        """Return instance if present and delete it from storage.
        """
        instance = self._storage.pop(uuid, None)

        if instance is None:
            return instance

        if not self._storage:
            self._statistics.clear()
            self._known_tags.clear()
            return

        # now we need to recalculate statistics
        self._statistics.clear()
        self._known_tags.clear()

        total_items = 0
        total_size = 0
        min_date = self._statistics['min_date']
        max_date = self._statistics['max_date']

        for record in self._storage.values():
            total_items += 1
            total_size += record.bytes_in_file
            min_date = min(min_date, record.registered_at)
            max_date = max(max_date, record.registered_at)
            self._known_tags.update(record.tags)

        self._statistics = {
            'total_items': total_items,
            'total_size': total_size,
            'min_date': min_date,
            'max_date': max_date,
        }
