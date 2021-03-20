# -*- coding: utf-8 -*-

"""Tool for UUID refreshing.
"""
import os

from mss.core.helper_types.class_filesystem import Filesystem
from mss.utils.utils_scripts import greet, ask


def main():
    """Entry point."""
    greet('UUID refreshing tool')

    filesystem = Filesystem()
    theme_directory = ask('Theme directory')
    meta_path = filesystem.join(theme_directory, 'metainfo')
    names = [x[:-5] for x in filesystem.list_files(meta_path)]
    names.sort()

    file_path = os.path.join(theme_directory, 'used_uuids.csv')
    with open(file_path, mode='w', encoding='utf-8') as file:
        for name in names:
            file.write(name + '\n')

    print(f'Written {len(names)} records')


if __name__ == '__main__':
    main()
