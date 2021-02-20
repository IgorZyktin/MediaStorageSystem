import json
import os

from PIL import Image

from register import settings


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


if __name__ == '__main__':
    fix_tags()
