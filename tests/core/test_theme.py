# -*- coding: utf-8 -*-

"""Tests.
"""


def test_theme_repr(theme):
    assert str(theme) == "Theme<directory='test_dir'>"


def test_theme_sorting(theme, theme_another):
    themes = [theme, theme_another]
    themes.sort()
    assert themes == [theme_another, theme]
