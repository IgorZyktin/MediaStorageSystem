# -*- coding: utf-8 -*-

"""Single metarecord, corresponds to a single json file.

Example of JSON form:
{
    "uuid": "008a2494-a6a4-4d63-886d-9e050f7a0d4a"
    "content": {
        "content_path": "root\\images\\magazines\\...",
        "preview_path": "root\\previews\\images\\magazines\\...",
        "thumbnail_path": "root\\thumbnails\\images\\magazines\\...",
    },
    "file_info": {
        "original_filename": "bubble_gum_crisis_-_b-club_special_-__130.jpg",
        "original_name": "bubble_gum_crisis_-_b-club_special_-__130",
        "ext": "jpg",
    },
    "meta": {
        "series": "bgc",
        "sub_series": "b-club special"
        "ordering": 132,
        "comment": "please note that this book ...",
    },
    "parameters": {
        "width": 2484
        "height": 3471,
        "resolution_mp": 8.62,
        "media_type": "static_image",
        "size": 564556,
    },
    "registration": {
        "registered_at": "2021-02-20",
        "registered_by_username": "Igor Zyktin",
        "registered_by_nickname": "Nicord",
    },
    "tags": [],
}
"""
from copy import deepcopy
from functools import cached_property
from typing import List, Dict, Union, Set

from common import synonims

JSON = Dict[str, Union[int, float, str, dict, list, None]]


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

            if isinstance(value, type(self)):
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


class Metarecord(Serializable):
    """Single metarecord, corresponds to a single json file.
    """

    def __init__(self, uuid: str, content_info: JSON, file_info: JSON,
                 meta: JSON, parameters: JSON, registration: JSON,
                 tags: List[str], **kwargs) -> None:
        """Initialize instance.
        """
        self.uuid = uuid
        self.content_info = ContentInfo(**content_info)
        self.file_info = FileInfo(**file_info)
        self.meta = Meta(**meta)
        self.parameters = Parameters(**parameters)
        self.registration = Registration(**registration)
        self.tags = tags
        self.kwargs = kwargs

    def __repr__(self) -> str:
        """Return textual representation.
        """
        return (f'{type(self).__name__}'
                f'<uuid={self.uuid}, {self.file_info.original_filename!r}>')

    @property
    def unique_filename(self) -> str:
        """Return base filename with uuid added.
        """
        return (f'{self.file_info.original_name}'
                f'___{self.uuid}.{self.file_info.ext}')

    @cached_property
    def tags_set(self) -> Set[str]:
        """Return tags of the record as a set of strings.
        """
        return set(self.tags)

    @cached_property
    def extended_tags_set(self) -> Set[str]:
        """Return tags of the record and anything tag-like.
        """
        extended_tags = {
            *self.tags_set,
            self.meta.series,
            self.meta.sub_series,
        }
        synonims.extend_tags_with_synonyms(extended_tags)
        return extended_tags
