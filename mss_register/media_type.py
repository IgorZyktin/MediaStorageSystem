# -*- coding: utf-8 -*-

"""Container for any media type.
"""
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

    def __init__(self, uuid: str, path: str, filename: str) -> None:
        """Initialize instance.
        """
        self.uuid = uuid
        self.path = path
        self.parameters = dict()

        self.original_filename = filename

        self.original_name, self.original_extension = \
            utils_filesystem.split_extension(self.original_filename)

        self.media_type = 'unknown'
        self.unique_filename = (self.original_name + '___'
                                + self.uuid + '.' + self.original_extension)
        self.content = None

    def __repr__(self) -> str:
        """Return textual representation.
        """
        return f'{type(self).__name__}(uuid={self.uuid}, path={self.path!r})'

    def analyze(self) -> bool:
        """Get metainfo for this media, return True if we can handle it.
        """
        tool = analyze.get_analyze_tool(self.original_extension)

        if not tool:
            return False

        self.media_type, self.content, self.parameters = tool(self)
        return True

    def to_metainfo(self) -> Dict[str, Any]:
        """Get metainfo for this media.
        """
        global total
        total += 1

        # TODO ----------------------------------------------------------------
        series = 'kenichi sonoda'
        sub_series = 'gallant'
        ordering = total
        group_name = 'gallant works gallant'
        group_members = []
        comment = """""".strip()
        tags = ['kenichi sonoda', 'artbook', 'artwork', 'gallant']
        # TODO ----------------------------------------------------------------

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

        return {
            'uuid': self.uuid,
            'path_to_content': cut_root(content_path),
            'path_to_preview': cut_root(preview_path),
            'path_to_thumbnail': cut_root(thumbnail_path),
            'original_filename': self.original_filename,
            'original_name': self.original_name,
            'original_extension': self.original_extension,
            'series': series,
            'sub_series': sub_series,
            'ordering': ordering,
            'next_record': '',
            'previous_record': '',
            'group_name': group_name,
            'group_members': group_members,

            **self.parameters,

            'registered_on': str(datetime.now().date()),
            'registered_by_username': '',
            'registered_by_nickname': '',
            'author': 'Kenichi Sonoda',
            'author_url': '',
            'origin_url': '',
            'comment': comment,

            'signature': '',
            'signature_type': '',

            'tags': tags,
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
