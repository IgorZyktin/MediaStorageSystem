# -*- coding: utf-8 -*-

"""Abstract storage for metarecords.
"""
import abc
from typing import Optional, Iterable, Set, Tuple

from mss.core.abstract_types.class_abstract_meta import AbstractMeta


class AbstractRepository(abc.ABC):
    """Abstract storage for metarecords.
    """

    @abc.abstractmethod
    def __contains__(self, uuid: str) -> bool:
        """Return True if uuid is in our storage.
        """

    @abc.abstractmethod
    def __repr__(self) -> str:
        """Return textual representation.
        """

    @abc.abstractmethod
    def __len__(self) -> int:
        """Return amount of records in repository.
        """

    @abc.abstractmethod
    def __iter__(self) -> Iterable[Tuple[str, AbstractMeta]]:
        """Iterate on records.
        """

    @abc.abstractmethod
    def add_record(self, new_record: AbstractMeta,
                   extended_tags: Optional[Set[str]] = None) -> None:
        """Add record into repository.

        :raises: ValueError if record already exist.
        """

    @abc.abstractmethod
    def get_record(self, uuid: str) -> Optional[AbstractMeta]:
        """Return record or None if not present.
        """

    @abc.abstractmethod
    def delete_record(self, uuid: str) -> Optional[AbstractMeta]:
        """Return instance if present and delete it from storage.
        """

    @abc.abstractmethod
    def all_uuids(self) -> Iterable[str]:
        """Return UUIDs in the storage.
        """

    @abc.abstractmethod
    def all_records(self) -> Iterable[AbstractMeta]:
        """Return records in the storage.
        """

    @abc.abstractmethod
    def all_items(self) -> Iterable[Tuple[str, AbstractMeta]]:
        """Return all uuid+record from the storage.
        """

    @abc.abstractmethod
    def get_uuids_by_tag(self, tag: str) -> Set[str]:
        """Return all UUIDs with this tag.
        """

    @abc.abstractmethod
    def get_extended_tags(self, uuid: str) -> Set[str]:
        """Return extended tags for given record UUID.
        """

    @abc.abstractmethod
    def clear(self) -> None:
        """Drop all records.
        """
