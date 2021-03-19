# -*- coding: utf-8 -*-

"""Special class that works with filesystem.
"""
import os
from typing import List


class Filesystem:
    """Special class that works with filesystem.
    """

    def __init__(self, root_folder: str) -> None:
        """Initialize instance."""
        self.root_folder = self.absolute(root_folder)

    @staticmethod
    def read_file(path: str) -> str:
        """Read textual file from the disk."""
        try:
            with open(path, mode='r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            content = ''
        return content

    @staticmethod
    def write_file(path: str, content: str) -> None:
        """Write textual file to the disk."""
        with open(path, mode='w', encoding='utf-8') as file:
            file.write(content)

    @staticmethod
    def join(*args) -> str:
        """Join path for specific filesystem.
        """
        return os.path.join(*args)

    @staticmethod
    def list_files(path: str) -> List[str]:
        """Enlist all files in given directory.
        """
        return [
            x for x in os.listdir(path)
            if os.path.isfile(os.path.join(path, x))
        ]

    @staticmethod
    def list_folders(path: str) -> List[str]:
        """Enlist all folders in given directory.
        """
        return [
            x for x in os.listdir(path)
            if os.path.isdir(os.path.join(path, x))
        ]

    @staticmethod
    def absolute(path: str) -> str:
        """Return absolute path.
        """
        return os.path.abspath(path)
