# -*- coding: utf-8 -*-

"""Non user friendly script.
"""
from mss.core.class_filesystem import Filesystem


def update_by_condition(root_path: str, theme: str):
    """Change records by condition."""
    fs = Filesystem()
    path = fs.join(root_path, theme, 'metainfo')

    for folder, filename, name, ext in fs.iter_ext(path):
        modified = False
        if ext != '.json':
            continue

        full_path = fs.join(folder, filename)
        content = fs.read_json(full_path)

        for uuid, record in content.items():
            if record['group_name'] == 'grand mal 1 rus':
                record['sub_series'] = 'grand mal 1 rus'
                modified = True

        if modified:
            fs.write_json(full_path, content)
            print(f'Modified: {full_path}')


if __name__ == '__main__':
    update_by_condition(
        root_path='D:\\BGC_ARCHIVE_TARGET\\',
        theme='bubblegum_crisis',
    )
