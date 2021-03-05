# -*- coding: utf-8 -*-

"""Main file.
"""
import json
import os
import shutil
from typing import Set

from common import utils_filesystem
from mss_register_remote import settings, interaction, network, analyze
from mss_register_remote.interaction import get_basic_description


def main():
    """Entry point.
    """
    existing_uuids = utils_filesystem.get_existing_filenames(
        path=settings.METAINFO_PATH
    )

    while True:
        mode = input('Enter anything for group handling').strip()

        if mode:
            print('--> Group handling')
            group_handling(existing_uuids)
        else:
            print('--> Single handling')
            single_handling(existing_uuids)

        print('-' * settings.TERMINAL_WIDTH)


def single_handling(existing_uuids: Set[str]) -> None:
    """Add one record.
    """
    path_elements = interaction.ask_list('Path elements')
    sub_path = utils_filesystem.join(*path_elements)

    meta = get_basic_description(existing_uuids)
    download_url = interaction.ask('Download URL')

    tmp_path = utils_filesystem.join(os.path.abspath(os.getcwd()),
                                     settings.TMP_PATH)
    path, filename = network.download_file(download_url, tmp_path)
    name, extension = utils_filesystem.split_extension(filename)

    new_name = f'{name}___{meta["uuid"]}.{extension}'
    new_name_meta = f'{meta["uuid"]}.json'

    meta['original_name'] = name
    meta['original_filename'] = filename
    meta['original_extension'] = extension

    meta['path_to_content'] = utils_filesystem.join('root', sub_path, new_name)
    meta['path_to_preview'] = utils_filesystem.join('root', 'previews',
                                                    sub_path, new_name)
    meta['path_to_thumbnail'] = utils_filesystem.join('root', 'thumbnails',
                                                      sub_path, new_name)

    tool = analyze.get_analyze_tool(extension)
    if not tool:
        raise

    image, parameters = tool(path)
    meta.update(parameters)

    actual_path_to_content = utils_filesystem.join(settings.BASE_PATH,
                                                   meta['path_to_content'])
    actual_path_to_preview = utils_filesystem.join(settings.BASE_PATH,
                                                   meta['path_to_preview'])
    actual_path_to_thumbnail = utils_filesystem.join(settings.BASE_PATH,
                                                     meta['path_to_thumbnail'])

    utils_filesystem.ensure_folder_exists(
        utils_filesystem.join(settings.BASE_PATH, 'root', sub_path)
    )
    shutil.copy(path, actual_path_to_content)

    meta_path = os.path.join(settings.METAINFO_PATH, new_name_meta)
    with open(meta_path, mode='w', encoding='utf-8') as file:
        json.dump(meta, file, indent=4, ensure_ascii=False)
        print(meta_path)

    if actual_path_to_preview:
        utils_filesystem.ensure_folder_exists(
            utils_filesystem.join(settings.PREVIEWS_PATH, sub_path)
        )
        new = image.copy()
        new.thumbnail(settings.PREVIEW_SIZE)
        new.save(actual_path_to_preview)

    if actual_path_to_thumbnail:
        utils_filesystem.ensure_folder_exists(
            utils_filesystem.join(settings.THUMBNAILS_PATH, sub_path)
        )
        new = image.copy()
        new.thumbnail(settings.THUMBNAIL_SIZE)
        new.save(actual_path_to_thumbnail)

    print('File written', meta_path)


def group_handling(existing_uuids: Set[str]) -> None:
    """Add many records as a single group.
    """


if __name__ == '__main__':
    main()
