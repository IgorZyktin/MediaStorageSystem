# -*- coding: utf-8 -*-

"""Non user friendly script.
"""
import json

from mss.core.class_filesystem import Filesystem


def update_all_used_uuids(root_path: str):
    """Update all used_uuids.csv files."""
    fs = Filesystem()

    themes = fs.list_folders(root_path)
    for theme in themes:
        path = fs.join(root_path, theme, 'metainfo')
        local_uuids = set()
        for filename in fs.list_files(path):
            if not filename.endswith('.json'):
                continue

            full_path = fs.join(root_path, theme, 'metainfo', filename)
            text = fs.read_file(full_path)
            content = json.loads(text)
            local_uuids.update(content.keys())

        uuids = sorted(local_uuids)

        if uuids:
            csv_path = fs.join(root_path, theme, 'used_uuids.csv')
            text = '\n'.join(uuids)
            fs.write_file(csv_path, text)
            print(f'Wrote: {csv_path}')


if __name__ == '__main__':
    update_all_used_uuids(
        root_path='D:\\PycharmProjects\\MediaStorageSystem\\example',
    )
