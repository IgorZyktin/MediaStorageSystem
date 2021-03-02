# -*- coding: utf-8 -*-

"""Class for search enhancement.
"""
from typing import Set

from core.class_imeta import IMeta

UNKNOWN = 'UNKNOWN'

# image sizes
TINY = 'TINY'
SMALL = 'SMALL'
MEAN = 'MEAN'
BIG = 'BIG'
HUGE = 'HUGE'
IMAGE_SIZES = {TINY, SMALL, MEAN, BIG, HUGE}

# duration types
SHORT = 'SHORT'
MID = 'MID'
LONG = 'LONG'
DURATION_TYPES = {SHORT, MID, LONG}

# media types
IMAGE = 'IMAGE'
GIF = 'GIF'
VIDEO = 'VIDEO'
AUDIO = 'AUDIO'
MEDIA_TYPES = {IMAGE, GIF, VIDEO, AUDIO}

# search keywords
DESC = 'DESC'
SEARCH_KEYWORDS = {DESC}

KEYWORDS = IMAGE_SIZES & DURATION_TYPES & MEDIA_TYPES & SEARCH_KEYWORDS


class SearchEnhancer:
    """Class for search enhancement.
    """

    def __init__(self, synonyms: dict = None) -> None:
        """Initialize instance.
        """
        self._synonyms = {}

        if synonyms:
            for comment, group in synonyms.items():
                self._synonyms[comment] = set(group)

    def get_extended_tags(self, record: IMeta) -> Set[str]:
        """Get base tags with additional words for search.
        """
        return {
            *(tag.lower() for tag in record.tags),
            record.uuid,
            record.series,
            record.sub_series,
            record.group_name,
            record.author,
            record.registered_on,
            self.get_image_size_tag(record.resolution),
            self.get_duration_tag(record.seconds),
            self.get_media_type_tag(record.media_type),
        }

    def get_extended_tags_with_synonyms(self, record: IMeta) -> Set[str]:
        """Get extended + synonyms for search.
        """
        extended_tags = self.get_extended_tags(record)
        additional_tags = set()

        for group in self._synonyms.values():
            for tag in extended_tags:
                if tag in group:
                    additional_tags.update(group)

        return extended_tags.union(additional_tags)

    @staticmethod
    def get_image_size_tag(resolution: float) -> str:
        """Get textual identifier for image size.
        """
        if 0 <= resolution < 0.1:
            return 'TINY'

        if 0.1 <= resolution < 1.0:
            return 'SMALL'

        if 1.0 <= resolution < 5.0:
            return 'MEAN'

        if 5.0 <= resolution < 10.0:
            return 'BIG'

        if resolution >= 10.0:
            return 'HUGE'

        return UNKNOWN

    @staticmethod
    def get_duration_tag(seconds: int) -> str:
        """Get textual identifier for media length.
        """
        if 0 <= seconds < 0.1:
            return 'SHORT'

        if 300 <= seconds < 1200:
            return 'MID'

        if seconds > 1200:
            return 'LONG'

        return UNKNOWN

    @staticmethod
    def get_media_type_tag(media_type: str) -> str:
        """Get textual identifier for media type.
        """
        return {
            'static_image': 'IMAGE',
            'animated_image': 'GIF',
            'video': 'VIDEO',
            'audio': 'AUDIO',
        }.get(media_type, UNKNOWN)
