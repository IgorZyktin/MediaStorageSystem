# -*- coding: utf-8 -*-

"""Tool for adding many items.
"""
import json

from mss import constants
from mss.core.helper_types.class_filesystem import Filesystem
from mss.utils.utils_identity import get_new_uuid
from mss.utils.utils_scripts import greet, get_existing_uuids, \
    iterate_on_filenames_of_ext, drop_filename_from_path
from mss_register.media_type import UnregisteredMedia


def main():
    """Entry point."""
    greet('Bulk adding tool')

    filesystem = Filesystem()
    # source = ask('Source directory')
    # root_path = ask('Root directory')
    # theme = ask('Theme')

    target_root_dir = 'D:\\BGC_ARCHIVE\\'
    source_root_dir = 'D:\\BGC_ARCHIVE_\\science_fiction\\'
    theme = 'science_fiction'
    target_theme_dir = filesystem.join(target_root_dir, theme)

    filesystem.ensure_folder_exists(source_root_dir)
    filesystem.ensure_folder_exists(target_theme_dir)

    uuids = get_existing_uuids(target_root_dir, filesystem)
    extensions = {'.jpg', '.jpeg', '.png'}

    for folder, filename in iterate_on_filenames_of_ext(source_root_dir,
                                                        extensions):
        uuid = get_new_uuid(uuids)
        original_path = filesystem.join(folder, filename)
        media = UnregisteredMedia(uuid, original_path, filename)
        correct = media.analyze()

        if correct:
            register(media, theme, target_theme_dir, original_path, filesystem)
            print(filename)
            # utils_filesystem.delete(path)


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

    with open(metainfo_path, mode='w') as file:
        json.dump(metainfo, file, indent=4, ensure_ascii=False)

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
