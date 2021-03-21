# -*- coding: utf-8 -*-

"""Container for any media type.
"""
from datetime import datetime
from typing import Dict, Any

from common import utils_filesystem
from mss.utils.utils_scripts import get_path_ending, drop_filename_from_path
from mss_register import analyze

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

    def to_metainfo(self, target_dir, theme, filesystem) -> Dict[str, Any]:
        """Get metainfo for this media.
        """
        global total
        total += 1

        # TODO ----------------------------------------------------------------
        series = 'cyberpunk 2077'
        sub_series = 'the world of cyberpunk 2077'
        ordering = total
        group_name = 'the world of cyberpunk 2077'
        group_members = []
        comment = """""".strip()
        tags = ['artbook', 'cyberpunk 2077', 'game']
        author = 'CD Project RED, Dark Horse'
        # TODO ----------------------------------------------------------------

        trace = get_path_ending(self.path, theme)
        trace = drop_filename_from_path(trace, self.original_filename)

        content_path = filesystem.join(target_dir,
                                       trace,
                                       self.unique_filename)

        thumbnail_path = filesystem.join(target_dir,
                                         'thumbnails',
                                         trace,
                                         self.unique_filename)

        preview_path = filesystem.join(target_dir,
                                       'previews',
                                       trace,
                                       self.unique_filename)

        return {
            'uuid': self.uuid,
            'path_to_content': get_path_ending(content_path, theme),
            'path_to_preview': get_path_ending(preview_path, theme),
            'path_to_thumbnail': get_path_ending(thumbnail_path, theme),
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
            'author': author,
            'author_url': '',
            'origin_url': '',
            'comment': comment,

            'signature': '',
            'signature_type': '',

            'tags': tags,
        }
