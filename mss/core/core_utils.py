# -*- coding: utf-8 -*-

"""Utils for the core functionality.
"""
from mss import core


def meta_sorter(meta: core.Meta) -> tuple:
    """Return some tuple we can sort on.
    """
    return (
        meta.series,
        meta.sub_series,
        meta.group_name,
        meta.ordering,
    )
