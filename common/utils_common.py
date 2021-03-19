# -*- coding: utf-8 -*-

"""Basic utils.
"""

from colorama import Fore


def output(*args, color: str = '', **kwargs) -> None:
    """Wrapper for print function.
    """
    if color:
        print(color, *args, Fore.RESET, **kwargs)
        return
    print(*args, **kwargs)
