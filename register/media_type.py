# -*- coding: utf-8 -*-

"""Container for any media type.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from common import utils_filesystem
from register import analyze, settings

# FIXME
total = 0


class Media:
    """Container for any media type.
    """

    def __init__(self, uuid: str, path: str,
                 tags: Optional[List[str]] = None,
                 parameters: Optional[Dict[str, Any]] = None) -> None:
        """Initialize instance.
        """
        self.uuid = uuid
        self.path = path
        self.tags = tags or []
        self.parameters = parameters if parameters else dict()

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

        comment = """please note that this book came to me with random filenames; pages 2, 33, 112 and 113 are kindof guesses
""".strip()

        return {
            'uuid': self.uuid,
            'description': self.description,
            'original_filename': self.original_filename,
            'original_name': self.name,
            'media_type': self.media_type,
            'content_path': cut_root(content_path),
            'thumbnail_path': cut_root(thumbnail_path),
            'preview_path': cut_root(preview_path),
            'ext': self.ext,
            'tags': self.tags,
            'parameters': self.parameters,
            'registered_at': str(datetime.now().date()),
            'registered_by': 'Igor Zyktin___Nicord',
            'meta': {
                'series': 'bgc',
                'sub_series': 'b-club special',
                'ordering': total,
                'comment': comment,
            },
        }

    def register(self) -> None:
        """Add this media to the storage.
        """
        metainfo = self.to_metainfo()
        metainfo_name = self.uuid + '.json'
        metainfo_path = utils_filesystem.join(settings.ROOT_PATH,
                                              'metainfo',
                                              metainfo_name)
        with open(metainfo_path, mode='w') as file:
            json.dump(metainfo, file)

        thumbnail_path = metainfo['thumbnail_path']
        thumbnail_path = thumbnail_path[5:]
        thumbnail_path = utils_filesystem.join(settings.ROOT_PATH, thumbnail_path)
        utils_filesystem.ensure_folder_exists(thumbnail_path)
        if thumbnail_path:
            new = self.content.copy()
            new.thumbnail(settings.THUMBNAIL_SIZE)
            new.save(thumbnail_path)

        preview_path = metainfo['preview_path']
        preview_path = preview_path[5:]
        preview_path = utils_filesystem.join(settings.ROOT_PATH, preview_path)
        utils_filesystem.ensure_folder_exists(preview_path)
        if preview_path:
            new = self.content.copy()
            new.thumbnail(settings.PREVIEW_SIZE)
            new.save(preview_path)

        content_path = metainfo['content_path']
        content_path = content_path[5:]
        content_path = utils_filesystem.join(settings.ROOT_PATH, content_path)
        utils_filesystem.ensure_folder_exists(content_path)
        if content_path:
            self.content.save(content_path)
        print(self.path)

    def delete_source_file(self) -> None:
        """Delete original file using path.
        """
        # FIXME
        if '_mice' not in self.path:
            utils_filesystem.delete(self.path)
            # print(self.path)


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
