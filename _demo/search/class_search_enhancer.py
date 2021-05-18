# -*- coding: utf-8 -*-

"""Class for search enhancement.
"""
from typing import Set

from mss import constants
from _demo.extension_entities.class_synonyms import Synonyms
from mss.core.class_meta import Meta


class SearchEnhancer:
    """Class for search enhancement.
    """

    def __init__(self, synonyms: Synonyms) -> None:
        """Initialize instance."""
        self._synonyms = synonyms

    @staticmethod
    def get_extended_tags(record: Meta) -> Set[str]:
        """Get base tags with additional words for search."""
        return {
            *(tag.lower() for tag in record.tags),
            record.uuid,
            record.series,
            record.sub_series,
            record.group_name,
            record.author,
            record.registered_on,
            get_image_size_tag(record.resolution),
            get_duration_tag(record.seconds),
            get_media_type_tag(record.media_type),
        }

    def get_extended_tags_with_synonyms(self, record: Meta) -> Set[str]:
        """Get extended + synonyms for search."""
        base_tags = self.get_extended_tags(record)
        additional_tags = set()

        for group in self._synonyms:
            for tag in base_tags:
                if tag in group:
                    additional_tags.update(group)
                    continue

        return base_tags | additional_tags


def get_image_size_tag(resolution: float) -> str:
    """Get textual identifier for image size."""
    if 0 < resolution < constants.THRESHOLD_TINY:
        return constants.RES_TINY

    if constants.THRESHOLD_TINY <= resolution < constants.THRESHOLD_SMALL:
        return constants.RES_SMALL

    if constants.THRESHOLD_SMALL <= resolution < constants.THRESHOLD_MEAN:
        return constants.RES_MEAN

    if constants.THRESHOLD_MEAN <= resolution < constants.THRESHOLD_BIG:
        return constants.RES_BIG

    if resolution >= constants.THRESHOLD_BIG:
        return constants.RES_HUGE

    return constants.UNKNOWN


def get_duration_tag(seconds: int) -> str:
    """Get textual identifier for media length."""
    if 0 < seconds < constants.THRESHOLD_MOMENT:
        return constants.DUR_MOMENT

    if constants.THRESHOLD_MOMENT <= seconds < constants.THRESHOLD_SHORT:
        return constants.DUR_SHORT

    if constants.THRESHOLD_SHORT <= seconds < constants.THRESHOLD_MEDIUM:
        return constants.DUR_MEDIUM

    if seconds >= constants.THRESHOLD_MEDIUM:
        return constants.DUR_LONG

    return constants.UNKNOWN


def get_media_type_tag(media_type: str) -> str:
    """Get textual identifier for media type."""
    return {
        'static_image': constants.TYPE_IMAGE,
        'animated_image': constants.TYPE_GIF,
        'video': constants.TYPE_VIDEO,
        'audio': constants.TYPE_AUDIO,
    }.get(media_type, constants.UNKNOWN)
