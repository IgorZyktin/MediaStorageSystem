# -*- coding: utf-8 -*-

"""Tests.
"""

import pytest

from mss import constants
from mss.core.class_theme import Theme
from mss.core.class_theme_repository import ThemesRepository


def test_theme_repository_creation():
    inst = ThemesRepository()
    assert str(inst) == 'ThemesRepository()'


def test_theme_repository_adding(theme):
    inst = ThemesRepository()
    inst.add(theme)
    assert inst.get(theme.directory) is theme
    assert inst.get(theme.name) is theme


def test_theme_repository_double_add(theme):
    inst = ThemesRepository()
    inst.add(theme)

    msg = "Directory test_dir is already taken for " \
          "theme Theme<name='Testing theme', directory='test_dir'>"
    with pytest.raises(KeyError, match=msg):
        inst.add(theme)

    theme2 = Theme(
        name=theme.name,
        directory='test_dir_somewhere',
        synonyms=theme.synonyms,
        tags_on_demand=theme.tags_on_demand,
        statistics=theme.statistics,
        used_uuids={'a', 'b', 'c'},
    )

    msg = "Name Testing theme is already taken for " \
          "theme Theme<name='Testing theme', directory='test_dir'>"
    with pytest.raises(KeyError, match=msg):
        inst.add(theme2)


def test_theme_repository_iter(theme):
    inst = ThemesRepository()
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
