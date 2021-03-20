# -*- coding: utf-8 -*-

"""Tool for adding many items.
"""

from mss.core.helper_types.class_filesystem import Filesystem
from mss.utils.utils_identity import get_new_uuid
from mss.utils.utils_scripts import ask, greet, get_existing_uuids, \
    iterate_on_filenames_of_ext


def main():
    """Entry point."""
    greet('Bulk adding tool')

    filesystem = Filesystem()
    # source = ask('Source directory')
    # root_path = ask('Root directory')
    # theme = ask('Theme')

    source = 'D:\\BGC_ARCHIVE_\\gits'
    root_path = 'D:\\BGC_ARCHIVE\\'
    theme = 'cyberpunk'

    filesystem.ensure_folder_exists(source)
    filesystem.ensure_folder_exists(filesystem.join(root_path, theme))

    uuids = get_existing_uuids(root_path, filesystem)
    extensions = {'.jpg', '.jpeg', '.png'}

    for folder, filename in iterate_on_filenames_of_ext(source, extensions):
        uuid = get_new_uuid(uuids)
        path_to_new_file = filesystem.join(folder, filename)
        print(folder, filename)


if __name__ == '__main__':
    main()
