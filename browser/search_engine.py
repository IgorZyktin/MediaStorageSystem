import random


def build_query(raw_query: str) -> None:
    return None


def select_images(metainfo: dict, finder, amount):
    uuids = random.sample(metainfo.keys(), amount)

    objs = []
    for x in uuids:
        meta = metainfo[x]
        objs.append({
            'path': meta['thumbnail_path'].replace('\\', '/'),
            'preview': f'/preview/{x}',
        })
    return objs
