# -*- coding: utf-8 -*-

"""Tool for content extraction.
"""
import json

from mss.core.helper_types.class_filesystem import Filesystem
from mss.utils.utils_scripts import (
    ask, greet, perc, ask_list, relocate_by_uuid,
)


def main():
    """Entry point."""
    greet('Content extraction tool')

    filesystem = Filesystem()
    source = ask('Path to source theme')
    target = ask('Path to target theme')

    filesystem.ensure_folder_exists(source)
    filesystem.ensure_folder_exists(target)

    while True:
        keys = ask_list('Which keys you want to check')
        values = ask_list('Corresponding values')
        pairs = list(zip(keys, values))
        print('Resulting pairs:', pairs)
        conf = ask('Type 1 if this is correct')
        if conf == '1':
            break

    print('Finding uuids')
    chosen_uuids = []
    meta_path = filesystem.join(source, 'metainfo')
    for filename in perc(filesystem.list_files(meta_path)):
        full_path = filesystem.join(meta_path, filename)

        with open(full_path, mode='r', encoding='utf-8') as file:
            content = file.read()

        record = json.loads(content)

        cond = [record.get(key) == value for key, value in pairs]
        if all(cond):
            chosen_uuids.append(record['uuid'])

    print(f'Found {len(chosen_uuids)} matching records')

    for uuid in perc(chosen_uuids):
        relocate_by_uuid(uuid, source, target, filesystem)


if __name__ == '__main__':
    main()
