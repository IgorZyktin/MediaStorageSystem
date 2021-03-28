# -*- coding: utf-8 -*-

"""Non user friendly script.
"""

from mss.core.class_filesystem import Filesystem


def tie_together(root_path: str, theme: str, group_name: str):
    """Find records with same group id and mark them as group."""
    fs = Filesystem()
    path = fs.join(root_path, theme, 'metainfo')
    targets = []

    for folder, filename, name, ext in fs.iter_ext(path):
        if ext != '.json':
            continue

        full_path = fs.join(folder, filename)
        content = fs.read_json(full_path)

        for uuid, record in content.items():
            if record['group_name'] == group_name:
                targets.append((
                    full_path,
                    uuid,
                    record
                ))

    targets.sort(key=lambda x: x[2]['ordering'])
    uuids = [x[2]['uuid'] for x in targets]

    for i in range(len(targets)):
        path, uuid, content = targets[i]
        assert content['uuid'] == uuids[i]

        content['group_members'] = uuids

        if i == 0:
            content['previous_record'] = ''
            content['next_record'] = uuids[1]

        elif i == len(targets) - 1:
            content['previous_record'] = uuids[-2]
            content['next_record'] = ''

        else:
            content['previous_record'] = uuids[i - 1]
            content['next_record'] = uuids[i + 1]

    for path, uuid, content in targets:
        old_content = fs.read_json(path)
        old_content[uuid] = content
        fs.write_json(path, old_content)
        print(f'Modified: {path}')


if __name__ == '__main__':
    tie_together(
        root_path='D:\\BGC_ARCHIVE\\',
        theme='bubblegum_crisis',
        group_name='gregor kari nene hardsuit',
    )
