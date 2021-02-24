# -*- coding: utf-8 -*-

"""Main file.
"""
import json

from common import utils_identity
from common import utils_filesystem
from mss_register import settings
from mss_register.media_type import UnregisteredMedia


def main():
    """Entry point.
    """
    metainfo = utils_filesystem.get_metarecords(
        settings.METAINFO_PATH,
        settings.LOCAL_CHANGES_PATH,
        limit=-1,
    )
    existing_uuids = set(metainfo.keys())

    i = 0
    for path in utils_filesystem.iterate_over_new_content(
            settings.NEW_CONTENT_PATH,
            settings.SUPPORTED_EXTENSIONS
    ):
        i += 1
        uuid = utils_identity.get_new_uuid(existing_uuids)

        media = UnregisteredMedia(uuid, path)
        correct = media.analyze()

        # if i > 5:
        #     break

        if correct:
            register(media)
            print(path)
            # utils_filesystem.delete(path)


def register(media) -> None:
    """Add this media to the storage.
    """
    metainfo = media.to_metainfo()
    metainfo_name = media.uuid + '.json'
    metainfo_path = utils_filesystem.join(settings.ROOT_PATH,
                                          'metainfo',
                                          metainfo_name)

    with open(metainfo_path, mode='w') as file:
        json.dump(metainfo, file, indent=4, ensure_ascii=False)

    thumbnail_path = metainfo['content_info']['thumbnail_path']
    thumbnail_path = thumbnail_path[5:]
    thumbnail_path = utils_filesystem.join(settings.ROOT_PATH,
                                           thumbnail_path)

    utils_filesystem.ensure_folder_exists(thumbnail_path)
    if thumbnail_path:
        new = media.content.copy()
        new.thumbnail(settings.THUMBNAIL_SIZE)
        new.save(thumbnail_path)

    preview_path = metainfo['content_info']['preview_path']
    preview_path = preview_path[5:]
    preview_path = utils_filesystem.join(settings.ROOT_PATH, preview_path)
    utils_filesystem.ensure_folder_exists(preview_path)
    if preview_path:
        new = media.content.copy()
        new.thumbnail(settings.PREVIEW_SIZE)
        new.save(preview_path)

    content_path = metainfo['content_info']['content_path']
    content_path = content_path[5:]
    content_path = utils_filesystem.join(settings.ROOT_PATH, content_path)
    utils_filesystem.ensure_folder_exists(content_path)
    if content_path:
        media.content.save(content_path)


if __name__ == '__main__':
    main()
