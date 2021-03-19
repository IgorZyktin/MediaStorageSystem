import json
import os
import uuid

import requests

FOLDER = 'D:\\BGC_ARCHIVE_TMP\\GENERATED\\images\\fanart\\'


def get_uuid():
    return str(uuid.uuid4())


def download_file(url: str):
    r = requests.get(url)

    mark = url.find('?')
    if mark != -1:
        url = url[:mark]

    filename = url.rsplit('/', 1)[1]
    content = r.content
    path = os.path.join(FOLDER, filename)
    with open(path, mode='wb') as file:
        file.write(content)
    print('Скачан файл', filename)
    return path, filename


def ask(descr):
    while True:
        value = input(descr + ' >').strip()
        return value
        # conf = input('Введите 1 для подтверждения').strip()
        # if conf == '1':
        #     return value


def main():
    while True:
        mode = input('Введи что-нибудь для групповой обработки').strip()
        if mode:
            print('Начата групповая обработка')
            group_handling()
        else:
            print('Начата одиночная обработка')
            single_handling()

        print('Обработка шага закончена')
        print('-' * 80)


def group_handling():
    author = ask('Введите автора')
    author_url = ask('Введите ссылку на профиль автора')
    tags = ask('Введите теги через запятую')
    group_name = ask('Введите group_name')
    comment = ask('Введите комментарий')
    tags = [x.strip().lower() for x in tags.split(',')]

    targets = []

    while True:
        origin_url = ask('Введите ссылку на контент или -1 для остановки')
        download_url = ask('Введите ссылку для скачивания или -1 для остановки')

        if origin_url == '-1' or download_url == '-1':
            break

        path, filename = download_file(download_url)
        name, ext = filename.rsplit('.', maxsplit=1)
        _uuid = get_uuid()
        new_name = f'{name}___{_uuid}.{ext}'
        os.rename(path, os.path.join(FOLDER, new_name))

        targets.append({
            'uuid': _uuid,
            'original_filename': filename,
            'original_name': name,
            'original_extension': ext,
            'group_name': group_name,
            'author': author,
            'author_url': author_url,
            'origin_url': origin_url,
            'tags': tags,
            'comment': comment,

        })

    group_members = [x['uuid'] for x in targets]
    print(group_members)

    for i, target in enumerate(targets):
        target['group_members'] = group_members

        if i == 0 and targets:
            target['previous_record'] = None
            target['next_record'] = group_members[1]

        elif i == len(targets) - 1:
            target['previous_record'] = group_members[-2]
            target['next_record'] = None

        else:
            target['previous_record'] = group_members[i-1]
            target['next_record'] = group_members[i+1]

    for target in targets:
        _uuid = target['uuid']
        meta_path = os.path.join(FOLDER, f'{_uuid}.json')
        with open(meta_path, mode='w', encoding='utf-8') as file:
            json.dump(target, file, indent=4, ensure_ascii=False)

        print('Записан файл', meta_path)

    print('Закончена группа')


def single_handling():
    author = ask('Введите автора')
    author_url = ask('Введите ссылку на профиль автора')
    origin_url = ask('Введите ссылку на контент')
    download_url = ask('Введите ссылку для скачивания')
    tags = ask('Введите теги через запятую')
    comment = ask('Введите комментарий')

    path, filename = download_file(download_url)
    name, ext = filename.rsplit('.', maxsplit=1)
    _uuid = get_uuid()
    new_name = f'{name}___{_uuid}.{ext}'
    os.rename(path, os.path.join(FOLDER, new_name))

    meta_path = os.path.join(FOLDER, f'{_uuid}.json')
    with open(meta_path, mode='w', encoding='utf-8') as file:
        json.dump({
            'uuid': _uuid,
            'original_filename': filename,
            'original_name': name,
            'original_extension': ext,
            'group_name': '',
            'group_members': [],
            'previous_record': '',
            'next_record': '',
            'author': author,
            'author_url': author_url,
            'origin_url': origin_url,
            'tags': [x.strip().lower() for x in tags.split(',')],
            'comment': comment,
        }, file, indent=4, ensure_ascii=False)

    print('Записан файл', meta_path)


if __name__ == '__main__':
    main()
