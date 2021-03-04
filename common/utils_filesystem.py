# -*- coding: utf-8 -*-

"""Special utils created to work with filesystem.
"""
import json
import os
from pathlib import Path
from typing import List, Generator, Optional, Collection, Tuple

from colorama import Fore

from common import utils_common


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


def iterate_on_filenames_of_ext(*locations: str, extension: str = 'json'
                                ) -> Generator[Tuple[str, str], None, None]:
    """Iterate on all folders and yield paths and filenames of given ext.
    """
    for location in locations:
        if not os.path.exists(location):
            continue

        for filename in os.listdir(location):

            if not filename.endswith(extension):
                continue

            yield location, filename


def join(*args) -> str:
    """Use os.path.join to create joined path.
    """
    return os.path.join(*args)


def delete_file(path: str) -> None:
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

    for i, part in enumerate(parts):
        # definitely a file
        if '___' in part:
            continue

        # probably a file
        if '.' in part and i == len(parts) - 1:
            continue

        if current_path is None:
            current_path = part
        else:
            current_path = join(current_path, part)

        if not os.path.exists(current_path):
            os.mkdir(current_path)
            utils_common.output(f'New folder created: {current_path}',
                                color=Fore.MARGENTA)

    return current_path


def load_json(path: str, filename: str = '') -> dict:
    """Generic JSON loader.
    """
    if filename:
        path = join(path, filename)

    try:
        with open(path, mode='r', encoding='utf-8') as file:
            content = json.load(file)
    except FileNotFoundError:
        content = {}

    return content


def load_jsons(*locations: str, limit: int = -1) -> List[dict]:
    """Load raw JSONs from given directories.
    """
    all_jsons = []

    for path, filename in iterate_on_filenames_of_ext(*locations):
        content = load_json(path, filename)

        if content:
            all_jsons.append(content)

            if 0 < limit <= len(all_jsons):
                break

    return all_jsons


def load_textual_file(path: str, filename: str = '') -> str:
    """Generic textual file loader.
    """
    if filename:
        path = join(path, filename)

    try:
        with open(path, mode='r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        content = ''

    return content
