# -*- coding: utf-8 -*-

"""Tests.
"""


def test_theme_repr(theme):
    assert str(theme) == "Theme<name='Testing theme'>"


def test_theme_sorting(theme, theme_another):
    themes = [None, theme, theme_another]
    themes.sort()
    assert themes == [None, theme_another, theme]
