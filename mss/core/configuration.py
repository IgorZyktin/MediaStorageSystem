# -*- coding: utf-8 -*-

"""Tools to work with configuration.
"""
import configparser
from argparse import Namespace


def get_user_config(path: str) -> Namespace:
    """Get specific user settings.
    """
    config = configparser.ConfigParser()
    config.read(path)
    return Namespace(**dict(config['browser']))


class Config:
    def __init__(self, root_path, title, injection, themes):
        self.root_path = root_path
        self.title = title
        self.injection = injection
        self.themes = themes
