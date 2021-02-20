# -*- coding: utf-8 -*-

"""Tools to analyze media.
"""
from typing import Optional, Callable, Tuple

from PIL import Image


def analyze_static_image(media) -> Tuple[str, Image.Image, dict]:
    """Get parameters of a static image (no gif).
    """
    image: Image.Image = Image.open(media.path)

    width, height = image.size

    parameters = {
        'width': width,
        'height': height,
        'resolution_mp': round(width * height / 1_000_000, 2),
    }

    return 'static_image', image, parameters


def get_analyze_tool(ext: str) -> Optional[Callable]:
    """Return callable that can analyze this kind of files.
    """
    return {
        'jpg': analyze_static_image,
        'jpeg': analyze_static_image,
        'bmp': analyze_static_image,
        'png': analyze_static_image,
    }.get(ext)
