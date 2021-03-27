# -*- coding: utf-8 -*-

"""Non user friendly script.
"""
import json

from mss.core.helper_types.class_filesystem import Filesystem


def make_each_json_nested_with_uuid(root_path: str, theme: str):
    """Add one nesting levels to json file.

    Before:
    {
        'uuid': 'b', ...
    }

    After:
    {
        'b': {'uuid': 'b', ...}
    }
    """
    fs = Filesystem()
    path = fs.join(root_path, theme, 'metainfo')

    for directory, filename, _, ext in fs.iter_ext(path):
        if ext != '.json':
            continue

        full_path = fs.join(directory, filename)

        text = fs.read_file(full_path)
        content = json.loads(text)
        new_content = {
            content['uuid']: content
        }
        new_text = json.dumps(new_content, ensure_ascii=False, indent=4)
        fs.write_file(full_path, new_text)
        print(f'Altered file: {filename}')


if __name__ == '__main__':
    make_each_json_nested_with_uuid(
        root_path='D:\\PycharmProjects\\MediaStorageSystem\\example',
        theme='farm',
    )
