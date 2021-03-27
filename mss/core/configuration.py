# -*- coding: utf-8 -*-

"""Tools to work with configuration.
"""
from argparse import Namespace

import yaml

from mss import constants
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


def load_raw_user_config(filesystem: Filesystem, path: str) -> Namespace:
    """Load specific user settings from file."""
    text = filesystem.read_file(path)
    config = yaml.safe_load(text)
    return Namespace(**config)


def get_config(filesystem: Filesystem) -> Config:
    """Create config instance."""
    config_path = filesystem.join(*constants.CONFIG_PATH_COMPONENTS)
    user_config = load_raw_user_config(filesystem, config_path)

    inst = Config()
    inst.host = user_config.host
    inst.port = user_config.port
    inst.title = user_config.title
    inst.items_per_page = user_config.items_per_page
    inst.root_path = filesystem.absolute(user_config.root_path)
    inst.debug = user_config.debug

    if user_config.inject_code:
        injection_path = filesystem.join(*constants.INJECTION_PATH_COMPONENTS)
        inst.injection = filesystem.read_file(injection_path)

    return inst
