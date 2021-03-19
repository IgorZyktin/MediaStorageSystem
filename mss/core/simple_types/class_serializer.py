# -*- coding: utf-8 -*-

"""Serializes to and from dictionary.
"""
from typing import Type, Dict, Any, TypeVar

T = TypeVar('T')


class Serializer:
    """Serializes to and from dictionary.

    Mostly this class is built because I fear that some
    attributes will be missed in source data.
    """

    def __init__(self, target_type: Type[T]) -> None:
        """Initialize instance."""
        self.target_type = target_type
        self.argument_types = target_type.__annotations__.copy()

    def serialize(self, record: T) -> Dict[str, Any]:
        """Convert instance to some other form."""
        serialized = {}

        for key, valid_type in self.argument_types.items():
            try:
                value = getattr(record, key)
            except AttributeError:
                if hasattr(valid_type, '__origin__'):
                    value = []
                else:
                    value = valid_type()

            serialized[key] = value

        return serialized

    def from_source(self, **kwargs) -> T:
        """Create instance from some other form."""
        clean_args = {}

        for key, valid_type in self.argument_types.items():
            if key in kwargs:
                clean_args[key] = kwargs[key]
            else:
                if hasattr(valid_type, '__origin__'):
                    clean_args[key] = []
                else:
                    clean_args[key] = valid_type()

        return self.target_type(**clean_args)
