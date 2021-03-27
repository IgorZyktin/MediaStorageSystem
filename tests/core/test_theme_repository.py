# -*- coding: utf-8 -*-

"""Tests.
"""

import pytest

from mss import constants
from mss.core.class_theme import Theme
from mss.core.class_theme_repository import ThemeRepository


def test_theme_repository_creation():
    inst = ThemeRepository()
    assert str(inst) == 'ThemeRepository()'


def test_theme_repository_adding(theme):
    inst = ThemeRepository()
    inst.add(theme)
    assert inst.get(theme.directory) is theme


def test_theme_repository_double_add(theme):
    inst = ThemeRepository()
    inst.add(theme)

    msg = 'Directory test_dir is already taken for ' \
          "theme Theme<directory='test_dir'>"
    with pytest.raises(KeyError, match=msg):
        inst.add(theme)


def test_theme_repository_iter(theme):
    inst = ThemeRepository()
    inst.add(theme)

    theme2 = Theme(
        name='name',
        directory=constants.ALL_THEMES,
        synonyms=theme.synonyms,
        tags_on_demand=theme.tags_on_demand,
        statistics=theme.statistics,
        used_uuids=set(),
    )
    inst.add(theme2)
    assert list(inst) == [theme2, theme]
