import json
import os

from PIL import Image


def fix_thumbnail_size():
    folder = 'D:\\BGC_ARCHIVE\\example\\thumbnails'

    for path, dirs, files in os.walk(folder):
        for file in files:
            full_path = os.path.join(path, file)
            image = Image.open(full_path)
            image.thumbnail(settings.THUMBNAIL_SIZE)
            image.save(full_path)
            print(file)


def drop_by_key():
    folder = 'D:\\BGC_ARCHIVE\\example\\metainfo'

    for filename in iterate_on_files(folder):
        with open(filename, mode='r', encoding='utf-8') as file:
            content = json.load(file)

        if content['meta']['group_id'] == 'kenichi sonoda artworks 1983-1997':
            utils_filesystem.delete_file(filename)

        print(filename)
