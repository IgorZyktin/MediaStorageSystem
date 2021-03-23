# -*- coding: utf-8 -*-

"""Special utils created to work with filesystem.
"""
import os
from typing import Generator, Optional, Tuple, Collection


def split_extension(filename: str) -> Tuple[str, Optional[str]]:
    """Return filename with extension (if has one).
    """
    parts = filename.rsplit('.', maxsplit=1)

    if len(parts) != 2:
        return filename, None

    return parts[0].lower(), parts[1].lower()


def iterate_on_filenames_of_ext(*locations: str,
                                extensions: Collection[str] = ('json',)
                                ) -> Generator[Tuple[str, str], None, None]:
    """Iterate on all folders and yield paths and filenames of given ext.
    """
    supported_extensions = set(extensions)

    for location in locations:
        if not os.path.exists(location):
            continue

        for folder, _, files in os.walk(location):
            for filename in files:
                name, ext = split_extension(filename)

                if not ext or ext in supported_extensions:
                    yield folder, filename.lower()
