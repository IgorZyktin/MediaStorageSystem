# -*- coding: utf-8 -*-

"""Tools to work with configuration.
"""
import configparser
from argparse import Namespace

from mss.core.helper_types.class_filesystem import Filesystem


class Config:
    """Dummy class that holds state.
    """

    def __init__(self, root_path='', title='',
                 injection='', host='', port: int = 5000,
                 items_per_page: int = 0, debug: bool = False):
        """Initialize instance."""
        self.root_path = root_path
        self.title = title
        self.injection = injection
        self.host = host
        self.port = port
        self.items_per_page = items_per_page
        self.debug = debug


def load_raw_user_config(path: str) -> Namespace:
    """Load specific user settings from file."""
    config = configparser.ConfigParser()
    config.read(path)

    resulting_config = {}
    for key, value in config['browser'].items():
        if value.lower() == 'yes':
            resulting_config[key] = True
        elif value.lower() == 'no':
            resulting_config[key] = False
        elif value.isdigit():
            resulting_config[key] = int(value)
        else:
            resulting_config[key] = value

    return Namespace(**resulting_config)


def get_config(filesystem: Filesystem) -> Config:
    """Create config instance."""
    user_config = load_raw_user_config('config.ini')

    inst = Config()
    inst.host = user_config.host
    inst.port = user_config.port
    inst.title = user_config.title
    inst.items_per_page = user_config.items_per_page
    inst.root_path = filesystem.absolute(user_config.root_path)
    inst.debug = user_config.debug

    if user_config.inject_code:
        inst.injection = filesystem.read_file('injection.html')

    return inst
