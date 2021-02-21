# -*- coding: utf-8 -*-

"""Helper classes, created to construct metarecord class.
"""
from copy import deepcopy

from common.type_hints import JSON

__all__ = [
    'Serializable',
    'ContentInfo',
    'FileInfo',
    'Meta',
    'Parameters',
    'Registration',
]


class Serializable:
    """Base class that gives dict conversion ability.
    """

    def to_dict(self) -> JSON:
        """Convert instance to dict including attributes.
        """
        output = {}

        for key, value in self.__dict__.items():
            if key == 'kwargs':
                # You must specifically describe
                # attribute for it to be serializable
                continue

            if isinstance(value, Serializable):
                # our attribute is another serializeable object
                output[key] = value.to_dict()
            else:
                output[key] = deepcopy(value)

        return output


class ContentInfo(Serializable):
    """Helper class for content description.
    """

    def __init__(self, content_path: str, preview_path: str,
                 thumbnail_path: str, **kwargs) -> None:
        """Initialize instance.
        """
        self.content_path = content_path
        self.preview_path = preview_path
        self.thumbnail_path = thumbnail_path
        self.kwargs = kwargs

    def url_path(self, attribute: str) -> str:
        """Return browser compatible version of the path.
        """
        original_path = getattr(self, attribute, '')
        return original_path.replace('\\', '/')


class FileInfo(Serializable):
    """Helper class for file description.
    """

    def __init__(self, ext: str, original_name: str,
                 original_filename: str, **kwargs) -> None:
        """Initialize instance.
        """
        self.ext = ext
        self.original_name = original_name
        self.original_filename = original_filename
        self.kwargs = kwargs
        assert self.original_filename.endswith(self.ext)


class Meta(Serializable):
    """Helper class with meta information about the file.
    """

    def __init__(self, series: str, sub_series: str, ordering: int,
                 comment: str, **kwargs) -> None:
        """Initialize instance.
        """
        self.series = series
        self.sub_series = sub_series
        self.ordering = ordering
        self.comment = comment
        self.kwargs = kwargs

        # TODO - additional fields
        #  next - next file in group
        #  previous - previous file in group
        #  related - all other files in group


class Parameters(Serializable):
    """Helper class with specific file parameters.

    These parameters will be used in search queries.
    """

    def __init__(self, width: int, height: int, resolution_mp: float,
                 media_type: str, size: int, **kwargs) -> None:
        """Initialize instance.
        """
        self.width = width
        self.height = height
        self.resolution_mp = resolution_mp
        self.media_type = media_type
        self.size = size
        self.kwargs = kwargs


class Registration(Serializable):
    """Helper class with information about adding to the archive.
    """

    def __init__(self, registered_at: str, registered_by_username: str,
                 registered_by_nickname: str, **kwargs) -> None:
        """Initialize instance.
        """
        self.registered_at = registered_at
        self.registered_by_username = registered_by_username
        self.registered_by_nickname = registered_by_nickname
        self.kwargs = kwargs
