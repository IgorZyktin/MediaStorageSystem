import json
import os

from PIL import Image

from common import utils_filesystem
from mss_register import settings


def iterate_on_files(folder):
    for path, dirs, files in os.walk(folder):
        for file in files:
            full_path = os.path.join(path, file)
            yield full_path


def fix_thumbnail_size():
    folder = 'D:\\BGC_ARCHIVE\\root\\thumbnails'

    for path, dirs, files in os.walk(folder):
        for file in files:
            full_path = os.path.join(path, file)
            image = Image.open(full_path)
            image.thumbnail(settings.THUMBNAIL_SIZE)
            image.save(full_path)
            print(file)


def fix_tags():
    folder = 'D:\\BGC_ARCHIVE\\root\\metainfo'

    for filename in iterate_on_files(folder):
        print(filename)
        with open(filename, mode='r', encoding='utf-8') as file:
            content = json.load(file)

        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4,
                      sort_keys=True)


def tie_together():
    folder = 'D:\\BGC_ARCHIVE\\root\\metainfo'

    targets = []
    for filename in iterate_on_files(folder):
        with open(filename, mode='r', encoding='utf-8') as file:
            old_content = json.load(file)

        if old_content['group_name'] == 'gallant works gallant':
            targets.append((filename, old_content))

    targets.sort(key=lambda x: x[1]['ordering'])

    uuids = [x[1]['uuid'] for x in targets]

    for i in range(len(targets)):
        current = targets[i][1]

        assert current['uuid'] == uuids[i]

        current['group_members'] = uuids

        if i == 0:
            current['previous_record'] = ''
            current['next_record'] = uuids[1]

        elif i == len(targets) - 1:
            current['previous_record'] = uuids[-2]
            current['next_record'] = ''

        else:
            current['previous_record'] = uuids[i - 1]
            current['next_record'] = uuids[i + 1]

    for filename, content in targets:
        print(filename)

        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)


def fix_one_key():
    folder = 'D:\\BGC_ARCHIVE\\root\\metainfo'

    for filename in iterate_on_files(folder):
        print(filename)
        with open(filename, mode='r', encoding='utf-8') as file:
            content = file.read()

        content = content.replace(' null,', ' "",')

        with open(filename, mode='w', encoding='utf-8') as file:
            file.write(content)


def drop_by_key():
    folder = 'D:\\BGC_ARCHIVE\\root\\metainfo'

    for filename in iterate_on_files(folder):
        with open(filename, mode='r', encoding='utf-8') as file:
            content = json.load(file)

        if content['meta']['group_id'] == 'kenichi sonoda artworks 1983-1997':
            utils_filesystem.delete_file(filename)

        print(filename)


def update_structure():
    folder = 'D:\\BGC_ARCHIVE\\root\\metainfo'

    for filename in iterate_on_files(folder):
        print(filename)
        with open(filename, mode='r', encoding='utf-8') as file:
            old_content = json.load(file)

        new_content = {
            'uuid': old_content['uuid'],

            'path_to_content': old_content["content_info"]['content_path'],
            'path_to_preview': old_content["content_info"]['preview_path'],
            'path_to_thumbnail': old_content["content_info"]['thumbnail_path'],

            'original_filename': old_content['file_info']['original_filename'],
            'original_name': old_content['file_info']['original_name'],
            'original_extension': old_content['file_info']['ext'],

            'series': old_content['meta']['series'],
            'sub_series': old_content['meta']['sub_series'],

            'group_name': old_content['meta']['group_id'],
            'group_members': old_content['meta']['group_uuids'],
            'previous_record': old_content['meta']['previous_record'],
            'next_record': old_content['meta']['next_record'],
            'ordering': old_content['meta']['ordering'],

            'width': old_content['parameters']['width'],
            'height': old_content['parameters']['height'],
            'resolution': old_content['parameters']['resolution_mp'],
            'bytes_in_file': old_content['parameters']['size'],
            'seconds': 0,
            'media_type': old_content['parameters']['media_type'],

            'registered_on': old_content['registration']['registered_at'],
            'registered_by_username': old_content['registration']['registered_by_username'],
            'registered_by_nickname': old_content['registration']['registered_by_nickname'],
            'author': old_content['origin']['author'],
            'author_url': old_content['origin']['profile'],
            'origin_url': old_content['origin']['url'],
            'comment': old_content['meta']['comment'],

            'signature': '',
            'signature_type': '',

            'tags': old_content['tags'],
        }

        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump(new_content, file, ensure_ascii=False, indent=4)


def fix_something():
    folder = 'D:\\PycharmProjects\\MediaStorageSystem\\root\\metainfo'

    for filename in iterate_on_files(folder):
        print(filename)
        with open(filename, mode='r', encoding='utf-8') as file:
            content = json.load(file)

            content['series'] = 'cute mice'
            content['group_name'] = ''
            content['tags'] = []

        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    tie_together()
