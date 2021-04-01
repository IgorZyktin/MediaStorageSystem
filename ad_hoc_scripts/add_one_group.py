# -*- coding: utf-8 -*-

"""Non user friendly script.
"""
from dataclasses import asdict
from datetime import datetime

from colorama import init, Fore

from ad_hoc_scripts.analyze import get_analyze_tool
from ad_hoc_scripts.utils import sort_json_records_inplace, \
    tie_json_records_inplace
from mss import constants
from mss.core import Meta
from mss.core.class_filesystem import Filesystem
from mss.utils.utils_identity import get_new_uuid
from mss.utils.utils_scripts import get_existing_uuids

init(autoreset=True)


def add_one_group(source_root_path: str, target_root_path: str,
                  reference_root_path: str, theme_directory: str,
                  base_keys: dict) -> None:
    """Add bunch of files from source dir as a single group.
    """
    fs = Filesystem()
    uuids = {'abc'}
    uuids = get_existing_uuids(source_root_path,
                               target_root_path,
                               reference_root_path, filesystem=fs)
    print(f'Found {len(uuids)} uuids')

    source_theme_dir = fs.join(source_root_path, theme_directory)
    target_theme_dir = fs.join(target_root_path, theme_directory)

    files = []
    ordering = 0

    for directory, filename, name, ext in fs.iter_ext(source_theme_dir):
        if ext not in constants.SUPPORTED_EXTENSIONS:
            continue

        uuid = get_new_uuid(uuids)
        new_filename = f'{name}___{uuid}{ext}'
        source_file_path = fs.join(directory, filename)
        common_path = directory[len(source_theme_dir) + 1:]

        new_content_dir = common_path
        new_content_path = fs.join(new_content_dir, new_filename)

        new_preview_dir = fs.join('previews', common_path)
        new_preview_path = fs.join(new_preview_dir, new_filename)

        new_thumbnail_dir = fs.join('thumbnails', common_path)
        new_thumbnail_path = fs.join(new_thumbnail_dir, new_filename)

        fs.ensure_folder_exists(fs.join(target_theme_dir, new_content_dir))
        fs.ensure_folder_exists(fs.join(target_theme_dir, new_preview_dir))
        fs.ensure_folder_exists(fs.join(target_theme_dir, new_thumbnail_dir))

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
            **base_keys,
        )
        content = asdict(meta)
        content.pop('directory', None)
        tool = get_analyze_tool(content['original_extension'])

        if tool is None:
            print(Fore.RED + 'FAIL!')
            print(content)
            return

        _, image, parameters = tool(source_file_path)
        content.update(parameters)
        content['registered_on'] = str(datetime.now().date())
        content['original_extension'] = content['original_extension'].lstrip(
            '.')

        files.append((image, source_file_path, content))

        # if len(files) > 5:
        #     break

    records = [x[2] for x in files]
    sort_json_records_inplace(records)
    tie_json_records_inplace(records)

    meta_content = {}
    group_name = base_keys['group_name']
    meta_filename = group_name.lower().replace(' ', '_') + '.json'

    for image, source_file_path, content in files:
        meta_content[content['uuid']] = content

        thumbnail_path = fs.join(target_theme_dir,
                                 content['path_to_thumbnail'])
        print('thumbnail --->', thumbnail_path)
        new = image.copy()
        new.thumbnail(constants.THUMBNAIL_SIZE)
        new.save(thumbnail_path)
        content['path_to_thumbnail'] = content['path_to_thumbnail'] \
            .replace('\\', '/')

        preview_path = fs.join(target_theme_dir,
                               content['path_to_preview'])
        print('preview --->', preview_path)
        new = image.copy()
        new.thumbnail(constants.PREVIEW_SIZE)
        new.save(preview_path)
        content['path_to_preview'] = content['path_to_preview'] \
            .replace('\\', '/')

        content_path = fs.join(target_theme_dir,
                               content['path_to_content'])
        print('content --->', content_path)
        fs.copy_file(source_file_path, content_path)
        content['path_to_content'] = content['path_to_content'] \
            .replace('\\', '/')

        fs.delete_file(source_file_path)
        print(Fore.RED + f'Deleted file: {source_file_path}')
        print()

    fs.ensure_folder_exists(fs.join(target_theme_dir, 'metainfo'))
    meta_path = fs.join(target_theme_dir, 'metainfo', meta_filename)
    fs.write_json(meta_path, meta_content)

    uuids = sorted(meta_content.keys())
    csv_path = fs.join(target_theme_dir, 'used_uuids.csv')

    with open(csv_path, mode='a', encoding='utf-8') as file:
        for uuid in uuids:
            file.write(uuid + '\n')


if __name__ == '__main__':
    add_one_group(
        source_root_path='D:\\BGC_ARCHIVE_SOURCE\\',
        target_root_path='D:\\BGC_ARCHIVE_TARGET\\',
        reference_root_path='D:\\BGC_ARCHIVE\\',
        theme_directory='blade_runner',
        base_keys={
            'series': 'blade runner 2019',
            'sub_series': 'comic 02',
            'group_name': 'blade runner 2019 02',
            'author': '',
            'author_url': '',
            'origin_url': '',
            'tags': [
                "comics",
                "blade runner",
                "blade runner 2019",
            ]
        },
    )
