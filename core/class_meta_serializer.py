# -*- coding: utf-8 -*-

"""Metarecord serializer.
"""
from abc import ABC, abstractmethod

from core.class_imeta import IMeta


class AbstractSerializer(ABC):
    """Metarecord serializer.
    """

    @abstractmethod
    def serialize(self, record: IMeta):
        """Convert instance to some other form.
        """

    @abstractmethod
    def from_source(self, *args, **kwargs) -> IMeta:
        """Create instance from some other form.
        """


class DictSerializer(AbstractSerializer):
    """Metarecord to and from dict serializer.
    """
    default_factories = [

    ]

    def serialize(self, record: IMeta):
        """Convert instance to some other form.
        """
        valid_attributes = {x for x in dir(IMeta) if not x.startswith('_')}
        serialized = {}

        for key, value in vars(record).items():
            if key.startswith('_'):
                continue

            if key in valid_attributes:
                serialized[key] = value

            else:
                # TODO
                pass


        # return {key: value for }

    def from_source(self, *args, **kwargs) -> IMeta:
        """Create instance from some other form.
        """
