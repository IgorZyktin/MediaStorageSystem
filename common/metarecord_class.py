# -*- coding: utf-8 -*-

"""Single metarecord, corresponds to a single json file.

Example of JSON form:
{
    "uuid": "008a2494-a6a4-4d63-886d-9e050f7a0d4a",
    "content_info": {
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
        "sub_series": "b-club special",
        "ordering": 132,
        "comment": "please note that this book ...",
        "group_id": "bgc b-club special",
        "group_uuids": [
            "aa11a638-b369-45b8-9743-f67a33e40b45",
            "8f2e8475-3972-491b-b93d-f8a794392030",
        ],
        "next_record": "135668be-64c6-4254-80c7-bde5a56a3501",
        "previous_record": "0db7c6b0-957b-408b-930d-eb9825af78e3"
    },
    "parameters": {
        "width": 2484,
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
    "origin": {
        "author": "Somebody",
        "url": "https://...",
        "profile": "https://..."
    },
    "tags": [],
}
"""
from functools import cached_property
from typing import List, Set

from common import synonims
from common.metarecord_helpers import *
from common.type_hints import JSON

__all__ = [
    'Metarecord',
]


class Metarecord(Serializable):
    """Single metarecord, corresponds to a single json file.
    """

    def __init__(self, uuid: str, content_info: JSON, file_info: JSON,
                 meta: JSON, parameters: JSON, registration: JSON,
                 origin: JSON, tags: List[str], **kwargs) -> None:
        """Initialize instance.
        """
        self.uuid = uuid
        self.content_info = ContentInfo(**content_info)
        self.file_info = FileInfo(**file_info)
        self.meta = Meta(**meta)
        self.parameters = Parameters(**parameters)
        self.registration = Registration(**registration)
        self.origin = Origin(**origin)
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
