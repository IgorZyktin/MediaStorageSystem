# -*- coding: utf-8 -*-

"""Container for any media type.
"""
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from common import utils_filesystem
from register import analyze, settings


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
        self.tags = set(tags) if tags else set()
        self.parameters = parameters if parameters else dict()

        self.original_filename = utils_filesystem.get_filename(self.path)

        self.name, self.ext = utils_filesystem.split_extension(
            self.original_filename
        )
        self.media_type = 'unknown'
        self.description = ''
        self.content = None
        self.unique_filename = self.uuid + '___' + self.original_filename

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
        sub_parts = parts[2:-1]

        content_path = utils_filesystem.join(settings.ROOT_PATH,
                                             'images',
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
            'description': self.description,
            'original_filename': self.original_filename,
            'original_name': self.name,
            'media_type': self.media_type,
            'content_path': content_path,
            'thumbnail_path': thumbnail_path,
            'preview_path': preview_path,
            'ext': self.ext,
            'tags': sorted(self.tags),
            'parameters': self.parameters,
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
        utils_filesystem.ensure_folder_exists(thumbnail_path)
        if thumbnail_path:
            new = self.content.copy()
            new.thumbnail(settings.THUMBNAIL_SIZE)
            new.save(thumbnail_path)

        preview_path = metainfo['preview_path']
        utils_filesystem.ensure_folder_exists(preview_path)
        if preview_path:
            new = self.content.copy()
            new.thumbnail(settings.PREVIEW_SIZE)
            new.save(preview_path)

        content_path = metainfo['content_path']
        utils_filesystem.ensure_folder_exists(content_path)
        if content_path:
            self.content.save(content_path)

    def delete_source_file(self) -> None:
        """Delete original file using path.
        """
        # FIXME
        if '_mice' not in self.path:
            utils_filesystem.delete(self.path)
