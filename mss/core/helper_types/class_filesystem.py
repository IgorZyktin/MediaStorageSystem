# -*- coding: utf-8 -*-

"""Special class that works with filesystem.
"""
import os
import shutil
from pathlib import Path
from typing import List


class Filesystem:
    """Special class that works with filesystem.
    """

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
        """Join path for specific filesystem."""
        return os.path.join(*args)

    @staticmethod
    def only_dir(path: str) -> str:
        """Remove filename from full path."""
        parts = path.split(os.sep)
        return os.path.join(*parts[:-1])

    @staticmethod
    def list_files(path: str) -> List[str]:
        """Enlist all files in given directory."""
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

    @classmethod
    def ensure_folder_exists(cls, path: str) -> bool:
        """Create all chain of folders at given path.

        Return True if creation is successful.
        Do not give path to files to this method!
        """
        _path = Path(path)
        parts = list(_path.parts)
        current_path = None
        actually_created = False

        for part in parts:
            if current_path is None:
                current_path = part
            else:
                current_path = cls.join(current_path, part)

            if not os.path.exists(current_path):
                os.mkdir(current_path)
                print(f'New folder created: {current_path}')
                actually_created = True

        return actually_created

    @staticmethod
    def copy_file(source: str, target: str) -> None:
        """Copy file from source to target."""
        shutil.copy(source, target)

    @staticmethod
    def move_file(source: str, target: str) -> None:
        """Move file from source to target."""
        shutil.move(source, target)

    @staticmethod
    def delete_file(path: str) -> None:
        """Delete file."""
        os.remove(path)
