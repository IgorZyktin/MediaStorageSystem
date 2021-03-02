# -*- coding: utf-8 -*-

"""Basic utils.
"""
from typing import Dict, Callable, Any


def make_weight_sorter(weights: Dict[str, int]) -> Callable:
    """Factory for sorter functions.
    """

    def func(element: Any) -> int:
        """Sorter func.
        """
        return weights.get(element, -1)

    return func
