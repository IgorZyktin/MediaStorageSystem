# -*- coding: utf-8 -*-

"""Tool for simple text replacing.
"""

from mss.core.helper_types.class_filesystem import Filesystem
from mss.utils.utils_scripts import ask, greet, perc


def main():
    """Entry point."""
    greet('Text replacement tool')

    filesystem = Filesystem()
    path = ask('Target directory')
    text_in = ask(' What to replace')
    text_out = ask('What put instead')

    for filename in perc(filesystem.list_files(path)):
        full_path = filesystem.join(path, filename)

        with open(full_path, mode='r', encoding='utf-8') as file:
            content = file.read()

        if text_in in content:
            content = content.replace(text_in, text_out)

            with open(full_path, mode='w', encoding='utf-8') as file:
                file.write(content)


if __name__ == '__main__':
    main()
