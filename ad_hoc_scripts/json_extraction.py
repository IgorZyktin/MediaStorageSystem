# -*- coding: utf-8 -*-

"""Non user friendly script.
"""
import json

from mss.core.helper_types.class_filesystem import Filesystem


def extract_records_from_single_json_to_a_group(root_path: str, theme: str,
                                                group_name: str):
    """Extract data from a single json into a group one.

    Before:
        file1.json
        {
            'a': {'uuid': 'a', ...}
        }
        file2.json
        {
            'b': {'uuid': 'b', ...}
        }

    After:
        new_file.json
        {
            'a': {'uuid': 'a', ...}
            'b': {'uuid': 'b', ...}
        }
    """
    fs = Filesystem()
    path = fs.join(root_path, theme, 'metainfo')
    names_to_delete = []
    new_group_file_content = {}
    new_name = group_name.lower() + '.json'

    for directory, filename, _, ext in fs.iter_ext(path):
        if ext != '.json':
            continue

        if filename == new_name:
            continue

        full_path = fs.join(directory, filename)

        text = fs.read_file(full_path)
        content = json.loads(text)
        group_file = len(content) > 1
        has_matches = False

        for uuid, sub_content in content.copy().items():
            if sub_content['group_name'] == group_name:
                has_matches = True
                new_group_file_content[uuid] = sub_content
                del content[uuid]

        if has_matches and group_file:
            if content:
                # extracted content from group file
                new_text = json.dumps(content, ensure_ascii=False, indent=4)
                fs.write_file(full_path, new_text)
                print(f'Wrote altered group file: {filename}')

            else:
                # extracted content from group file and nothing left inside
                names_to_delete.append(full_path)

        elif has_matches and not group_file:
            # extracted content from single file
            names_to_delete.append(full_path)

    for path in names_to_delete:
        fs.delete_file(path)
        print(f'Delete file: {path}')

    if new_group_file_content:
        new_text = json.dumps(new_group_file_content,
                              ensure_ascii=False, indent=4)
        new_path = fs.join(root_path, theme, 'metainfo', new_name)
        fs.write_file(new_path, new_text)
        print(f'Created file: {new_name}')


if __name__ == '__main__':
    extract_records_from_single_json_to_a_group(
        root_path='D:\\PycharmProjects\\MediaStorageSystem\\example',
        theme='gerbils',
        group_name='whitey',
    )
