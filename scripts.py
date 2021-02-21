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


def fix_structure():
    folder = 'D:\\BGC_ARCHIVE\\root\\metainfo'

    for filename in iterate_on_files(folder):
        print(filename)
        with open(filename, mode='r', encoding='utf-8') as file:
            old_content = json.load(file)

        file_path = os.path.join('D:\\BGC_ARCHIVE\\', old_content['content_path'])
        size = os.path.getsize(file_path)

        new_content = {
            'uuid': old_content['uuid'],
            'content': {
                'content_path': old_content['content_path'],
                'preview_path': old_content['preview_path'],
                'thumbnail_path': old_content['thumbnail_path'],
            },
            'file_info': {
                'original_filename': old_content['original_filename'],
                'original_name': old_content['original_name'],
                'ext': old_content['ext'],
            },
            'meta': {
                'series': old_content['meta']['series'],
                'sub_series': old_content['meta']['sub_series'],
                'ordering': old_content['meta']['ordering'],
                'comment': old_content['meta'].get('comment'),
            },
            'parameters': {
                'width': old_content['parameters']['width'],
                'height': old_content['parameters']['height'],
                'resolution_mp': old_content['parameters']['resolution_mp'],
                'media_type': old_content['media_type'],
                'size': size,
            },
            'registration': {
                'registered_at': old_content['registered_at'],
                'registered_by_username': old_content['registered_by'].split('___')[0],
                'registered_by_nickname': old_content['registered_by'].split('___')[-1],
            },
            'tags': old_content['tags'],
        }
        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump(new_content, file, ensure_ascii=False, indent=4)


def fix_one_key():
    folder = 'D:\\BGC_ARCHIVE\\root\\metainfo'

    for filename in iterate_on_files(folder):
        print(filename)
        with open(filename, mode='r', encoding='utf-8') as file:
            content = file.read()

        content = content.replace("content", "content_info")

        with open(filename, mode='w', encoding='utf-8') as file:
            file.write(content)


if __name__ == '__main__':
    fix_one_key()
