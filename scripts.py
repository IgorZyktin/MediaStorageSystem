import json
import os

from PIL import Image

from mss_register import settings
from common import utils_filesystem


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
            json.dump(content, file, ensure_ascii=False, indent=4, sort_keys=True)


def tie_together():
    folder = 'D:\\BGC_ARCHIVE_\\root\\metainfo'

    targets = []
    for filename in iterate_on_files(folder):
        with open(filename, mode='r', encoding='utf-8') as file:
            old_content = json.load(file)

        if old_content['meta']['group_id'] == 'blade runner sketchbook':
            targets.append((filename, old_content))

    targets.sort(key=lambda x: x[1]['meta']['ordering'])

    uuids = [x[1]['uuid'] for x in targets]

    for i in range(len(targets)):
        current = targets[i][1]

        assert current['uuid'] == uuids[i]

        current['meta']['group_uuids'] = uuids

        if i == 0:
            current['meta']['previous_record'] = ''
            current['meta']['next_record'] = uuids[1]

        elif i == len(targets) - 1:
            current['meta']['previous_record'] = uuids[-2]
            current['meta']['next_record'] = ''

        else:
            current['meta']['previous_record'] = uuids[i - 1]
            current['meta']['next_record'] = uuids[i + 1]

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

        content = content.replace('"Igor Zyktin"', '""')
        content = content.replace('"Nicord"', '""')

        with open(filename, mode='w', encoding='utf-8') as file:
            file.write(content)


def drop_by_key():
    folder = 'D:\\BGC_ARCHIVE\\root\\metainfo'

    for filename in iterate_on_files(folder):
        with open(filename, mode='r', encoding='utf-8') as file:
            content = json.load(file)

        if content['meta']['group_id'] == 'kenichi sonoda artworks 1983-1997':
            utils_filesystem.delete(filename)

        print(filename)


if __name__ == '__main__':
    tie_together()
