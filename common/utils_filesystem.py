# -*- coding: utf-8 -*-

"""Special utils created to work with filesystem.
"""
import os
from collections import defaultdict
from pathlib import Path
from typing import List, Generator, Optional, Collection, Tuple, Dict

import json

from common.metarecord_class import Metarecord, Metainfo


def split_extension(filename: str) -> Tuple[str, Optional[str]]:
    """Return filename with extension (if has one).
    """
    parts = filename.rsplit('.', maxsplit=1)

    if len(parts) != 2:
        return filename, None

    return parts[0].lower(), parts[1].lower()


def iterate_over_filenames(sequence: List[str],
                           extensions: Optional[Collection[str]] = None
                           ) -> Generator[str, None, None]:
    """Yield filename or None if this extension is not what we're looking for.
    """
    extensions = set(extensions) if extensions else set()

    for element in sequence:
        filename, ext = split_extension(element)

        if ext and (not extensions or ext.lower() in extensions):
            yield filename.lower()


def iterate_over_new_content(path: str,
                             supported_extensions: Collection[str] = None
                             ) -> Generator[str, None, None]:
    """Yield paths for new content files.
    """
    supported_extensions = (set(supported_extensions)
                            if supported_extensions else set())

    for sub_path, dirs, files in os.walk(path):
        for filename in files:
            name, ext = split_extension(filename)

            if ext in supported_extensions:
                yield join(sub_path, filename)


def join(*args) -> str:
    """Use os.path.join to create joined path.
    """
    return os.path.join(*args)


def delete(path: str) -> None:
    """Delete file.
    """
    os.remove(path)


def get_filename(path: str) -> str:
    """Extract filename from path.
    """
    _, tail = os.path.split(path)
    return tail


def ensure_folder_exists(path: str) -> Optional[str]:
    """Create all subsequent sub paths for given path.
    """
    path = Path(path)
    parts = list(path.parts)
    current_path = None

    for part in parts:
        if '___' in part:
            continue

        if current_path is None:
            current_path = part
        else:
            current_path = join(current_path, part)

        if not os.path.exists(current_path):
            os.mkdir(current_path)
            print(f'New folder created: {current_path}')

    return current_path


def get_metarecords(*locations: str, limit: int = -1) -> Metainfo:
    """Load all metainfo as instances of Metarecord.
    """
    combined_metainfo = defaultdict(dict)

    for location in locations:
        for uuid, content in load_raw_metainfo(location).items():
            combined_metainfo[uuid].update(content)

            if 0 < limit <= len(combined_metainfo):
                break

    clean_metainfo = {}

    for uuid, content in combined_metainfo.items():
        clean_metainfo[uuid] = Metarecord(**content)

    return clean_metainfo


def load_raw_metainfo(folder: str, file_type: str = 'json') -> Dict[str, dict]:
    """Load metarecords as dicts from given folder.
    """
    if not os.path.exists(folder):
        return {}

    filenames = os.listdir(folder)
    metainfo = {}

    for filename in filenames:
        if filename.endswith(file_type):
            path = join(folder, filename)
            with open(path, mode='r', encoding='utf-8') as file:
                content = json.load(file)
                uuid = content['uuid']
                metainfo[uuid] = content

    return metainfo
