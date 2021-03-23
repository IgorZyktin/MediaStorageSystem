# -*- coding: utf-8 -*-

"""Tool for adding many items.
"""
import json
import os
from datetime import datetime

from ad_hoc_scripts.mss_register.media_type import UnregisteredMedia
from mss import constants
from mss.core.concrete_types import Meta
from mss.core.helper_types.class_filesystem import Filesystem
from mss.core.simple_types import Serializer
from mss.utils.utils_identity import get_new_uuid
from mss.utils.utils_scripts import greet, iterate_on_filenames_of_ext, \
    drop_filename_from_path, get_existing_uuids

SOURCE_ROOT = 'D:\\BGC_ARCHIVE_SOURCE\\'
TARGET_ROOT = 'D:\\BGC_ARCHIVE_TARGET\\'
REFERENCE_ROOT = 'D:\\BGC_ARCHIVE\\'
THEME = 'bubblegum_crisis'

EXTENSIONS = {'.jpg', '.jpeg', '.png'}
ORDERING = True
TIE_TOGETHER = True
serializer = Serializer(Meta)


def main():
    """Entry point."""
    greet('Bulk adding tool')

    filesystem = Filesystem()

    source_directory = filesystem.join(SOURCE_ROOT, THEME)
    target_directory = filesystem.join(TARGET_ROOT, THEME)

    filesystem.ensure_folder_exists(source_directory)
    filesystem.ensure_folder_exists(target_directory)

    uuids = get_existing_uuids(SOURCE_ROOT,
                               TARGET_ROOT,
                               REFERENCE_ROOT,
                               filesystem=filesystem)
    print(f'Found {len(uuids)} uuids')
    metas = get_metas(source_directory, uuids,
                      filesystem, ORDERING)
    print(f'Made {len(metas)} metas')

    for meta in metas:
        meta.group_name = ''

    for meta in metas:
        media = UnregisteredMedia(meta.uuid,
                                  meta.path_to_content,
                                  meta.original_filename)
        correct = media.analyze()

        if correct:
            register(media, THEME, target_directory,
                     meta.path_to_content, filesystem)
            print(meta)


def get_metas(source_directory, uuids, filesystem, ordering):
    metas = []
    number = 0
    for folder, filename in iterate_on_filenames_of_ext(source_directory,
                                                        EXTENSIONS):
        if ordering:
            number += 1
        uuid = get_new_uuid(uuids)
        uuids.add(uuid)
        source_path = filesystem.join(folder, filename)
        name, ext = os.path.splitext(filename)

        meta = serializer.from_source(
            uuid=uuid,
            path_to_content=source_path,
            path_to_preview='',
            path_to_thumbnail='',
            original_filename=filename,
            original_name=name,
            original_extension=ext,
            series='',
            sub_series='',
            ordering=number,
            registered_on=str(datetime.now().date()),
            tags=[]
        )
        metas.append(meta)
    return metas


def register(media, theme, target_theme_dir, original_path,
             filesystem) -> None:
    """Add this media to the storage.
    """
    filesystem.ensure_folder_exists(filesystem.join(target_theme_dir,
                                                    'metainfo'))
    filesystem.ensure_folder_exists(filesystem.join(target_theme_dir,
                                                    'images'))
    filesystem.ensure_folder_exists(filesystem.join(target_theme_dir,
                                                    'previews'))
    filesystem.ensure_folder_exists(filesystem.join(target_theme_dir,
                                                    'thumbnails'))

    metainfo = media.to_metainfo(target_theme_dir, theme, filesystem)
    metainfo_path = filesystem.join(target_theme_dir,
                                    'metainfo',
                                    media.uuid + '.json')

    metainfo2 = metainfo.copy()
    metainfo2['path_to_thumbnail'] = metainfo2['path_to_thumbnail'].replace('\\', '/')
    metainfo2['path_to_preview'] = metainfo2['path_to_preview'].replace('\\', '/')
    metainfo2['path_to_content'] = metainfo2['path_to_content'].replace('\\', '/')

    with open(metainfo_path, mode='w') as file:
        json.dump(metainfo2, file, indent=4, ensure_ascii=False)

    thumbnail_path = filesystem.join(target_theme_dir,
                                     metainfo['path_to_thumbnail'])
    _thumbnail_path = drop_filename_from_path(thumbnail_path,
                                              media.unique_filename)
    filesystem.ensure_folder_exists(_thumbnail_path)
    if _thumbnail_path:
        print('thumbnail --->', thumbnail_path)
        new = media.content.copy()
        new.thumbnail(constants.THUMBNAIL_SIZE)
        new.save(thumbnail_path)

    preview_path = filesystem.join(target_theme_dir,
                                   metainfo['path_to_preview'])
    _preview_path = drop_filename_from_path(preview_path,
                                            media.unique_filename)
    filesystem.ensure_folder_exists(_preview_path)
    if _preview_path:
        print('preview --->', preview_path)
        new = media.content.copy()
        new.thumbnail(constants.PREVIEW_SIZE)
        new.save(preview_path)

    content_path = filesystem.join(target_theme_dir,
                                   metainfo['path_to_content'])
    _content_path = drop_filename_from_path(content_path,
                                            media.unique_filename)
    filesystem.ensure_folder_exists(_content_path)
    if _content_path:
        print(original_path, '--->', content_path)
        filesystem.copy_file(original_path, content_path)


if __name__ == '__main__':
    main()
