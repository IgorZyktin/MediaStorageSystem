# -*- coding: utf-8 -*-

"""Container for any media type.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from common import utils_filesystem
from mss_register import analyze, settings

# FIXME
total = 0


class UnregisteredMedia:
    """Container for any media type.
    """

    def __init__(self, uuid: str, path: str) -> None:
        """Initialize instance.
        """
        self.uuid = uuid
        self.path = path
        self.parameters = dict()

        self.original_filename = utils_filesystem.get_filename(self.path)

        self.name, self.ext = utils_filesystem.split_extension(
            self.original_filename
        )
        self.media_type = 'unknown'
        self.description = ''
        self.content = None
        self.unique_filename = self.name + '___' + self.uuid + '.' + self.ext

    def __repr__(self) -> str:
        """Return textual representation.
        """
        return f'{type(self).__name__}(uuid={self.uuid}, path={self.path!r})'

    def analyze(self) -> bool:
        """Get metainfo for this media, return True if we can handle it.
        """
        tool = analyze.get_analyze_tool(self.ext)

        if not tool:
            return False

        self.media_type, self.content, self.parameters = tool(self)
        return True

    def to_metainfo(self) -> Dict[str, Any]:
        """Get metainfo for this media.
        """
        # TODO - what about thumbnails and previews for video and audio?
        parts = Path(self.path).parts

        sub_parts = []
        started = False
        for element in parts:
            if element == 'new_content':
                started = True
            elif not started:
                continue
            else:
                sub_parts.append(element)
        sub_parts = sub_parts[:-1]

        content_path = utils_filesystem.join(settings.ROOT_PATH,
                                             *sub_parts,
                                             self.unique_filename)

        thumbnail_path = utils_filesystem.join(settings.ROOT_PATH,
                                               'thumbnails',
                                               *sub_parts,
                                               self.unique_filename)

        preview_path = utils_filesystem.join(settings.ROOT_PATH,
                                             'previews',
                                             *sub_parts,
                                             self.unique_filename)
        global total
        total += 1

        comment = """""".strip()

        return {
            'uuid': self.uuid,
            'content_info': {
                'content_path': cut_root(content_path),
                'thumbnail_path': cut_root(thumbnail_path),
                'preview_path': cut_root(preview_path),
            },
            'file_info': {
                'original_filename': self.original_filename,
                'original_name': self.name,
                'ext': self.ext,
            },
            'meta': {
                'series': 'kenichi sonoda',
                'sub_series': 'garden party',
                'ordering': total,
                'comment': comment,
                'group_id': 'kenichi sonoda garden party',
                'group_uuids': [],
                'next_record': '',
                'previous_record': '',
            },
            'parameters': self.parameters,
            'registration': {
                "registered_at": str(datetime.now().date()),
                "registered_by_username": "",
                "registered_by_nickname": "",
            },
            'origin': {
                "author": "Kenichi Sonoda",
                "url": "",
                "profile": ""
            },
            "tags": ['kenichi sonoda', 'artwork', 'artbook', 'garden party'],
        }


def cut_root(path) -> str:
    parts = list(Path(path).parts)
    final_parts = []
    started = False
    for element in parts:
        if element == 'root':
            started = True
        elif not started:
            continue
        final_parts.append(element)
    return utils_filesystem.join(*final_parts)
