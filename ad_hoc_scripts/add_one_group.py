# -*- coding: utf-8 -*-

"""Non user friendly script.
"""
import json
from dataclasses import asdict

from mss import constants
from mss.core import Meta
from mss.core.class_filesystem import Filesystem
from mss.utils.utils_identity import get_new_uuid


def add_one_group(source_path: str, target_path: str, reference_path: str,
                  theme: str, record: dict):
    """Add bunch of files from source dir as a single group.
    """
    fs = Filesystem()
    # uuids = get_existing_uuids(source_path,
    #                            target_path,
    #                            reference_path, filesystem=fs)
    uuids = {'abc'}
    print(f'Found {len(uuids)} uuids')

    source_theme = fs.join(source_path, theme)
    target_theme = fs.join(source_path, theme)

    files_to_delete = []
    meta_content = {}
    group_name = record['group_name']
    meta_filename = group_name.lower().replace(' ', '_') + '.json'

    ordering = 0
    for directory, filename, name, ext in fs.iter_ext(source_theme):
        if ext not in constants.SUPPORTED_EXTENSIONS:
            continue

        uuid = get_new_uuid(uuids)
        new_filename = f'{name}___{uuid}{ext}'

        original_path = fs.join(directory, filename)

        base_path = directory[len(source_theme):]

        new_content_path = fs.join(base_path,
                                   new_filename).replace('\\', '/')

        new_preview_path = fs.join('previews',
                                   base_path,
                                   new_filename).replace('\\', '/')

        new_thumbnail_path = fs.join('thumbnails',
                                     base_path,
                                     new_filename).replace('\\', '/')

        ordering += 1

        meta = Meta(
            uuid=uuid,
            original_filename=filename,
            original_name=name,
            original_extension=ext,

            path_to_content=new_content_path,
            path_to_preview=new_preview_path,
            path_to_thumbnail=new_thumbnail_path,

            ordering=ordering,
            **record,
        )
        content = asdict(meta)
        content.pop('directory', None)
        print(source_theme)
        print(directory, name, json.dumps(content, indent=4))
        break

    #     full_path = fs.join(directory, filename)
    #
    #     text = fs.read_file(full_path)
    #     content = json.loads(text)
    #     group_file = len(content) > 1
    #     has_matches = False
    #
    #     for uuid, sub_content in content.copy().items():
    #         if sub_content['group_name'] == group_name:
    #             has_matches = True
    #             meta_content[uuid] = sub_content
    #             del content[uuid]
    #
    #     if has_matches and group_file:
    #         if content:
    #             # extracted content from group file
    #             new_text = json.dumps(content, ensure_ascii=False, indent=4)
    #             fs.write_file(full_path, new_text)
    #             print(f'Wrote altered group file: {filename}')
    #
    #         else:
    #             # extracted content from group file and nothing left inside
    #             names_to_delete.append(full_path)
    #
    #     elif has_matches and not group_file:
    #         # extracted content from single file
    #         names_to_delete.append(full_path)
    #
    # for path in names_to_delete:
    #     fs.delete_file(path)
    #     print(f'Deleted file: {path}')
    # else:
    #     print()
    #
    # if meta_content:
    #     new_path = fs.join(root_path, theme, 'metainfo', meta_filename)
    #     fs.write_json(new_path, meta_content)
    #     print(f'Created file: {new_path}')


if __name__ == '__main__':
    add_one_group(
        source_path='D:\\BGC_ARCHIVE_SOURCE\\',
        target_path='D:\\BGC_ARCHIVE_TARGET\\',
        reference_path='D:\\BGC_ARCHIVE\\',
        theme='bubblegum_crisis',
        record={
            'series': 'bgc',
            'sub_series': 'comics',
            'group_name': 'grand mal 01',
            'author': 'Adam Warren',
            'author_url': 'https://www.deviantart.com/adamwarren',
            'origin_url': 'http://rutracker.org/forum/viewtopic.php?t=5225496',
        },
    )
