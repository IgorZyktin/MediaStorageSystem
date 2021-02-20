import random
import re

pat = re.compile(r'(\sAND\s|\sOR\s|\sNOT\s)')


class Finder:
    def __init__(self):
        self.and_ = set()
        self.not_ = set()
        self.or_ = set()

    def get_query(self):
        return ' '.join([
            *[f'OR {x}' for x in self.or_],
            *[f'AND {x}' for x in self.and_],
            *[f'NOT {x}' for x in self.not_],
        ])


def grouped(iterable, n):
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return zip(*[iter(iterable)] * n)


def build_query(raw_query: str) -> Finder:
    parts = pat.split(raw_query)
    parts = [x.strip() for x in parts if x.strip()]
    finder = Finder()
    if not parts:
        return finder
    if parts[0] not in ['AND', 'OR', 'NOT']:
        parts.insert(0, 'OR')

    for operator, operand in grouped(parts, 2):
        if operator == 'OR':
            finder.or_.add(operand)
        elif operator == 'AND':
            finder.and_.add(operand)
        elif operator == 'NOT':
            finder.not_.add(operand)

    return finder


def select_images(metainfo: dict, finder, amount):
    chosen = []

    if not finder.and_ and not finder.or_ and not finder.not_:
        uuids = random.sample(metainfo.keys(), min(amount, len(metainfo)))
        chosen = [(x, metainfo[x]) for x in uuids]
    else:
        for uuid, meta in metainfo.items():
            tags = {*meta['tags'],
                    meta['meta']['series'],
                    meta['meta']['sub_series']}

            if (finder.and_ & tags == finder.and_ or not finder.and_) \
                    and (not finder.not_ & tags or not finder.not_) \
                    and (finder.or_ & tags or not finder.or_):
                chosen.append((uuid, meta))

    def s(x):
        return (
            x[1]['meta'].get('series'),
            x[1]['meta'].get('sub_series'),
            x[1]['meta'].get('ordering'),
        )

    chosen.sort(key=s)
    objs = []
    for uuid, meta in chosen[:amount]:
        objs.append({
            'path': meta['thumbnail_path'].replace('\\', '/'),
            'preview': f'/preview/{uuid}',
        })
    return len(chosen), objs
