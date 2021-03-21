import json
import os
from datetime import datetime

from PIL import Image

from mss_register import settings

FOLDER = 'D:\\BGC_ARCHIVE_TMP\\GENERATED\\images\\fanart\\'
SOURCE = 'D:\\BGC_ARCHIVE_TMP\\GENERATED\\'
ROOT = 'D:\\BGC_ARCHIVE_TMP\\GENERATED\\example'


def ifiles():
    for fold, dirs, files in os.walk(SOURCE):
        for file in files:
            if file.endswith('.json'):
                yield os.path.join(fold, file)


def get_full_path(target):
    for fold, dirs, files in os.walk(SOURCE):
        for file in files:
            if file == target:
                return os.path.join(fold, file)
    return None


def main():
    for path in ifiles():

        with open(path, mode='r', encoding='utf-8') as file:
            content = json.load(file)

        if content['original_extension'] != 'png':
            continue

        filename = content['original_name'] + '___' + content['uuid'] + '.' + \
                   content['original_extension']
        full_path = get_full_path(filename)

        if not full_path:
            print('не найден путь для', filename)
            continue

        base = full_path.replace(SOURCE, '')

        image = Image.open(full_path)

        width, height = image.size
        size = os.path.getsize(full_path)

        image.save(os.path.join(ROOT, base))

        image.thumbnail(settings.PREVIEW_SIZE)
        image.save(os.path.join(ROOT, 'previews', base))

        image.thumbnail(settings.THUMBNAIL_SIZE)
        image.save(os.path.join(ROOT, 'thumbnails', base))

        image.close()

        clean_content = {
            "uuid": content['uuid'],
            "content_info": {
                "content_path": f"example\\{base}",
                "preview_path": f"example\\previews\\{base}",
                "thumbnail_path": f"example\\thumbnails\\{base}"
            },
            "file_info": {
                "original_filename": content['original_filename'],
                "original_name": content['original_name'],
                "ext": content['original_extension']
            },
            "meta": {
                "series": "",
                "sub_series": "",
                "ordering": -1,
                "comment": content.get('comment', ''),
                "group_id": content.get('group_name', ''),
                "group_uuids": content.get('group_members', ''),
                "next_record": content.get('next_record', ''),
                "previous_record": content.get('previous_record', ''),
            },
            "parameters": {
                "width": width,
                "height": height,
                "resolution_mp": round(width * height / 1_000_000, 2),
                "media_type": "static_image",
                "size": size,
            },
            "registration": {
                "registered_at": str(datetime.now().date()),
                "registered_by_username": "",
                "registered_by_nickname": ""
            },
            "tags": content['tags'],
            "origin": {
                "author": content['author'],
                "url": content['origin_url'],
                "profile": content['author_url']
            }
        }

        meta_path = os.path.join(ROOT, 'metainfo', content['uuid'] + '.json')
        with open(meta_path, mode='w', encoding='utf-8') as file:
            json.dump(clean_content, file, indent=4, ensure_ascii=False)

        print(meta_path)

        os.rename(full_path, full_path + '_______')
        os.rename(path, path + '_______')


if __name__ == '__main__':
    main()
