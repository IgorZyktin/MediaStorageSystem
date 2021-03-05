# -*- coding: utf-8 -*-

"""Tools to analyze media.
"""
import os
from typing import Optional, Callable, Tuple

from PIL import Image


def analyze_static_image(path: str) -> Tuple[Image.Image, dict]:
    """Get parameters of a static image (no gif).
    """
    image: Image.Image = Image.open(path)

    width, height = image.size

    parameters = {
        'width': width,
        'height': height,
        'resolution': round(width * height / 1_000_000, 2),
        'media_type': 'static_image',
        'bytes_in_file': os.path.getsize(path),
        'seconds': 0,
    }

    return image, parameters


def get_analyze_tool(extension: str) -> Optional[Callable]:
    """Return callable that can analyze this kind of files.
    """
    return {
        'jpg': analyze_static_image,
        'jpeg': analyze_static_image,
        'bmp': analyze_static_image,
        'png': analyze_static_image,
    }.get(extension.lower())
