# -*- coding: utf-8 -*-

"""Common script tools.
"""
import json
import os
from typing import List, Iterable, Generator, Set

from mss import constants, core


def greet(description: str) -> None:
    """Print greeting message."""
    print(description.center(constants.TERMINAL_WIDTH, '~'))
    print('-' * constants.TERMINAL_WIDTH)


def ask(description: str, confirm: bool = False) -> str:
    """Ask something from user."""
    while True:
        value = input(description + ' >').strip()

        if confirm:
            while True:
                conf = input('Enter 1 for confirm and 0 to retry').strip()

                if conf == '1':
                    return value

                if conf == '0':
                    break

        return value


def ask_list(description: str, sep: str = ',',
             confirm: bool = False) -> List[str]:
    """Ask sequence of words from user."""
    text = ask(description, confirm)
    return [x.strip() for x in text.split(sep)]


def perc(iterable: Iterable) -> Generator:
    """Iterate with progress bar."""
    collection = list(iterable)
    total = len(collection)

    for i, element in enumerate(collection, start=1):
        percent = i / total * 100
        ending = f'{percent:0.1f} %'.rjust(7, ' ')
        total_chars = constants.TERMINAL_WIDTH - len(ending) - 3
        complete = '#' * int(total_chars * percent / 100)
        left = '_' * (total_chars - len(complete))

        print(f'\r[{complete}{left}] {ending}', end='')
        yield element
    print()


# pylint: disable=R0914
def relocate_by_uuid(uuid: str, source_theme_path: str,
                     target_theme_path: str,
                     filesystem: core.Filesystem) -> None:
    """Relocate whole tree of resources by its UUID."""
    meta_path = filesystem.join(source_theme_path, 'metainfo', f'{uuid}.json')
    content = filesystem.read_file(meta_path)
    record = json.loads(content)

    path_to_content = record['path_to_content']
    path_to_preview = record['path_to_preview']
    path_to_thumbnail = record['path_to_thumbnail']

    dir_content = filesystem.cut_tail(path_to_content)
    dir_preview = filesystem.cut_tail(path_to_preview)
    dir_thumbnail = filesystem.cut_tail(path_to_thumbnail)

    target_content = filesystem.join(target_theme_path, dir_content)
    target_preview = filesystem.join(target_theme_path, dir_preview)
    target_thumbnail = filesystem.join(target_theme_path, dir_thumbnail)

    filesystem.ensure_folder_exists(target_content)
    filesystem.ensure_folder_exists(target_preview)
    filesystem.ensure_folder_exists(target_thumbnail)
    filesystem.ensure_folder_exists(filesystem.join(target_theme_path,
                                                    'metainfo'))
    name = record['original_name']
    ext = record['original_extension']
    filename = f'{name}___{uuid}.{ext}'

    filesystem.move_file(
        filesystem.join(source_theme_path, path_to_content),
        filesystem.join(target_content, filename)
    )

    filesystem.move_file(
        filesystem.join(source_theme_path, path_to_preview),
        filesystem.join(target_preview, filename)
    )

    filesystem.move_file(
        filesystem.join(source_theme_path, path_to_thumbnail),
        filesystem.join(target_thumbnail, filename)
    )

    filesystem.move_file(
        filesystem.join(meta_path),
        filesystem.join(target_theme_path, 'metainfo', f'{uuid}.json')
    )

    uuids_file = filesystem.join(target_theme_path, 'used_uuids.csv')
    with open(uuids_file, mode='a', encoding='utf-8') as file:
        file.write(uuid + '\n')


def get_existing_uuids(*root_paths: str,
                       filesystem: core.Filesystem) -> Set[str]:
    """Get all existing UUIDs."""
    found_uuids = set()

    for root_path in root_paths:
        themes = filesystem.list_folders(root_path)

        for theme in themes:
            path = filesystem.join(root_path, theme, 'used_uuids.csv')

            if not os.path.exists(path):
                continue

            content = filesystem.read_file(path)

            if content:
                uuids = [x.strip() for x in content.split('\n')]
                found_uuids.update(uuids)

    return found_uuids


def get_path_ending(path: str, pivot: str) -> str:
    """Blah"""
    parts = path.split(os.sep)
    for i, element in enumerate(parts):
        if element == pivot:
            return os.sep.join(parts[i + 1:])
    return path


def drop_filename_from_path(path: str, filename: str) -> str:
    """
    >>> drop_filename_from_path(r'C:\\users\\test.txt', 'test.txt')
    'C:\\users\\'
    """
    if path.endswith(filename):
        return path[:-len(filename)]
    return path
