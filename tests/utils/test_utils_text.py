# -*- coding: utf-8 -*-

"""Tests.
"""
from mss.utils.utils_text import byte_count_to_text, sep_digits


def test_byte_count_to_text_ru():
    """Must convert to readable size in russian."""
    f = byte_count_to_text
    assert f(-2_000, language='RU') == '-2.0 КиБ'
    assert f(-2_048, language='RU') == '-2.0 КиБ'
    assert f(0, language='RU') == '0 Б'
    assert f(27, language='RU') == '27 Б'
    assert f(999, language='RU') == '999 Б'
    assert f(1_000, language='RU') == '1000 Б'
    assert f(1_023, language='RU') == '1023 Б'
    assert f(1_024, language='RU') == '1.0 КиБ'
    assert f(1_728, language='RU') == '1.7 КиБ'
    assert f(110_592, language='RU') == '108.0 КиБ'
    assert f(1_000_000, language='RU') == '976.6 КиБ'
    assert f(7_077_888, language='RU') == '6.8 МиБ'
    assert f(452_984_832, language='RU') == '432.0 МиБ'
    assert f(1_000_000_000, language='RU') == '953.7 МиБ'
    assert f(28_991_029_248, language='RU') == '27.0 ГиБ'
    assert f(1_855_425_871_872, language='RU') == '1.7 ТиБ'
    assert f(9_223_372_036_854_775_807, language='RU') == '8.0 ЭиБ'


def test_byte_count_to_text_en():
    """Must convert to readable size in english."""
    f = byte_count_to_text
    assert f(-2_000, language='EN') == '-2.0 KiB'
    assert f(-2_048, language='EN') == '-2.0 KiB'
    assert f(0, language='EN') == '0 B'
    assert f(27, language='EN') == '27 B'
    assert f(999, language='EN') == '999 B'
    assert f(1_000, language='EN') == '1000 B'
    assert f(1_023, language='EN') == '1023 B'
    assert f(1_024, language='EN') == '1.0 KiB'
    assert f(1_728, language='EN') == '1.7 KiB'
    assert f(110_592, language='EN') == '108.0 KiB'
    assert f(1_000_000, language='EN') == '976.6 KiB'
    assert f(7_077_888, language='EN') == '6.8 MiB'
    assert f(452_984_832, language='EN') == '432.0 MiB'
    assert f(1_000_000_000, language='EN') == '953.7 MiB'
    assert f(28_991_029_248, language='EN') == '27.0 GiB'
    assert f(1_855_425_871_872, language='EN') == '1.7 TiB'
    assert f(9_223_372_036_854_775_807, language='EN') == '8.0 EiB'


def test_sep_digits():
    """Must separate digits on 1000s."""
    f = sep_digits
    assert f('12345678') == '12345678'
    assert f(12345678) == '12 345 678'
    assert f(1234.5678) == '1 234.57'
    assert f(1234.5678, precision=4) == '1 234.5678'
    assert f(1234.0, precision=4) == '1 234.0000'
    assert f(1234.0, precision=0) == '1 234'
