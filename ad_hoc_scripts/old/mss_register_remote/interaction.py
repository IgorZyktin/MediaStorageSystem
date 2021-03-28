# -*- coding: utf-8 -*-

"""Tools to interact with user.
"""
from typing import List, Set

from mss.utils import utils_identity
from ad_hoc_scripts.old.mss_register_remote import metageneration


def ask(description: str, strict: bool = False) -> str:
    """Ask for user input with description.

    If strict==True, then user must confirm given input.
    """
    while True:
        value = input(description + ' >').strip()

        if strict:
            confirmation = input('Enter 1 for confirmation').strip()
            if confirmation != '1':
                continue

        return value
    return ''


def ask_list(description: str, separator: str = ',',
             strict: bool = False) -> List[str]:
    """Ask user for list of things.
    """
    string = ask(description + f'("{separator}" separated)', strict=strict)
    elements = [
        x.strip().lower()
        for x in string.split(separator)
    ]
    return elements


def get_basic_description(existing_uuids: Set[str]) -> dict:
    """General handle for the record.
    """
    series = ask('Series')
    sub_series = ask('Sub series')

    author = ask('Author name')
    author_url = ask('Author profile URL')
    origin_url = ask('Media page URL')
    tags = ask_list('Tags')
    comment = ask('Comment')

    uuid = utils_identity.get_new_uuid(existing_uuids)

    meta = metageneration.make_metainfo_from_kw(
        uuid=uuid,
        series=series,
        sub_series=sub_series,
        author=author,
        author_url=author_url,
        origin_url=origin_url,
        tags=tags,
        comment=comment,
    )
    return meta
