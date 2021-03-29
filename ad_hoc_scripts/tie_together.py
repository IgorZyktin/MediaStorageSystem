# -*- coding: utf-8 -*-

"""Non user friendly script.
"""
from ad_hoc_scripts.utils import (
    sort_json_records_inplace,
    tie_json_records_inplace,
)
from mss.core.class_filesystem import Filesystem


def tie_together(root_path: str, theme: str, group_name: str):
    """Find records with same group id and mark them as group."""
    fs = Filesystem()
    path = fs.join(root_path, theme, 'metainfo')
    records = []

    for folder, filename, name, ext in fs.iter_ext(path):
        if ext != '.json':
            continue

        full_path = fs.join(folder, filename)
        content = fs.read_json(full_path)

        for uuid, record in content.items():
            if record['group_name'] == group_name:
                record['_full_path'] = full_path
                records.append(record)

    sort_json_records_inplace(records)
    tie_json_records_inplace(records)

    for record in records:
        uuid = record['uuid']
        path = record.pop('_full_path')

        old_record = fs.read_json(path)
        old_record[uuid] = record
        fs.write_json(path, old_record)
        print(f'Modified: {path}')


if __name__ == '__main__':
    tie_together(
        root_path='D:\\BGC_ARCHIVE\\',
        theme='bubblegum_crisis',
        group_name='gregor kari nene hardsuit',
    )
