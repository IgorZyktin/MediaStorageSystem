import random
import re

OPERATORS = {
    'AND',
    'OR',
    'NOT',
}

string = '|'.join(r'\s+{}\s+'.format(x) for x in OPERATORS)
pat = re.compile('(' + string + ')')


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


def make_searching_machine(raw_query: str) -> Finder:
    parts = pat.split(raw_query)
    parts = [x.strip() for x in parts if x.strip()]
    finder = Finder()
    if not parts:
        return finder

    if parts[0] not in OPERATORS:
        parts.insert(0, 'OR')

    for operator, operand in grouped(parts, 2):
        if operator == 'OR' or operand == '?':
            finder.or_.add(operand)
        elif operator == 'AND' or operator == '+':
            finder.and_.add(operand)
        elif operator == 'NOT' or operator == '-':
            finder.not_.add(operand)

    return finder


def s(x):
    return (
        x[1].meta.series,
        x[1].meta.sub_series,
        x[1].meta.ordering,
    )


def select_random_images(metainfo: dict, items_per_page):
    uuids = random.sample(metainfo.keys(), min(items_per_page, len(metainfo)))
    chosen = [(x, metainfo[x]) for x in uuids]

    chosen.sort(key=s)

    return [x[1] for x in chosen]


def select_images(metainfo: dict, searching_machine):
    chosen = []

    for uuid, meta in metainfo.items():
        tags = meta.extended_tags_set

        if (
                searching_machine.and_ & tags == searching_machine.and_ or not searching_machine.and_) \
                and (
                not searching_machine.not_ & tags or not searching_machine.not_) \
                and (
                searching_machine.or_ & tags or not searching_machine.or_):
            chosen.append((uuid, meta))

    chosen.sort(key=s)

    return [x[1] for x in chosen]
