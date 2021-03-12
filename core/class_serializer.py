# -*- coding: utf-8 -*-

"""Metarecord serializer.
"""
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Union, TypeVar, Type

from core.class_abstract_meta import AbstractMeta

T = TypeVar('T', bound=AbstractMeta)


class AbstractSerializer(ABC):
    """Metarecord serializer.
    """

    def __init__(self, target_type: Type[T]):
        """Initialize instance.
        """
        self.target_type = target_type

    @abstractmethod
    def serialize(self, record: T):
        """Convert instance to some other form.
        """

    @abstractmethod
    def from_source(self, *args, **kwargs) -> T:
        """Create instance from some other form.
        """


@lru_cache
def get_nonexistent_attribute(key: str) -> Union[int, str, list]:
    """Create new valid value for nonexistent attribute.
    """
    if key in ('tags', 'group_members'):
        value = []
    elif key in ('ordering', 'width', 'height',
                 'resolution', 'bytes_in_file', 'seconds'):
        value = -1
    else:
        value = ''

    return value


class DictSerializer(AbstractSerializer):
    """Metarecord to and from dict serializer.
    """
    valid_attributes = AbstractMeta.__annotations__.copy()

    def serialize(self, record: AbstractMeta):
        """Convert instance to some other form.
        """
        serialized = {}

        for key in self.valid_attributes:
            try:
                value = getattr(record, key)
            except AttributeError:
                value = get_nonexistent_attribute(key)

            serialized[key] = value

        return serialized

    def from_source(self, *args, **kwargs) -> AbstractMeta:
        """Create instance from some other form.
        """
        clean_args = {}
        for key in self.valid_attributes:
            if key in kwargs:
                clean_args[key] = kwargs[key]
            else:
                clean_args[key] = get_nonexistent_attribute(key)

        return self.target_type(**clean_args)
