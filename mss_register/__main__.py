# -*- coding: utf-8 -*-

"""Main file.
"""
import json
import os
from shutil import copyfile

from common import utils_filesystem
from mss.utils import utils_identity
from mss_register import settings
from mss_register.media_type import UnregisteredMedia


def main():
    """Entry point.
    """
    existing_uuids = utils_filesystem.get_existing_filenames(
        path=settings.METAINFO_PATH
    )

    for folder, filename in utils_filesystem.iterate_on_filenames_of_ext(
            settings.NEW_CONTENT_PATH,
            extensions=settings.SUPPORTED_EXTENSIONS
    ):
        uuid = utils_identity.get_new_uuid(existing_uuids)
        path = os.path.join(folder, filename)
        media = UnregisteredMedia(uuid, path, filename)
        correct = media.analyze()

        if correct:
            register(media, path, filename)
            print(path)
            # utils_filesystem.delete(path)


def register(media, path, filename) -> None:
    """Add this media to the storage.
    """
    metainfo = media.to_metainfo()
    metainfo_name = media.uuid + '.json'
    metainfo_path = utils_filesystem.join(settings.ROOT_PATH,
                                          'metainfo',
                                          metainfo_name)

    with open(metainfo_path, mode='w') as file:
        json.dump(metainfo, file, indent=4, ensure_ascii=False)

    thumbnail_path = metainfo['path_to_thumbnail']
    thumbnail_path = thumbnail_path[5:]
    thumbnail_path = utils_filesystem.join(settings.ROOT_PATH,
                                           thumbnail_path)

    utils_filesystem.ensure_folder_exists(thumbnail_path)
    if thumbnail_path:
        new = media.content.copy()
        new.thumbnail(settings.THUMBNAIL_SIZE)
        new.save(thumbnail_path)

    preview_path = metainfo['path_to_preview']
    preview_path = preview_path[5:]
    preview_path = utils_filesystem.join(settings.ROOT_PATH, preview_path)
    utils_filesystem.ensure_folder_exists(preview_path)
    if preview_path:
        new = media.content.copy()
        new.thumbnail(settings.PREVIEW_SIZE)
        new.save(preview_path)

    content_path = metainfo['path_to_content']
    content_path = content_path[5:]
    content_path = utils_filesystem.join(settings.ROOT_PATH, content_path)
    utils_filesystem.ensure_folder_exists(content_path)
    if content_path:
        copyfile(path, content_path)


if __name__ == '__main__':
    main()
