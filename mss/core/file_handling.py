# -*- coding: utf-8 -*-

"""Work with actual files using Filesystem class.
"""
import json
from typing import List, Optional

import yaml

from mss.core.class_repository import Repository
from mss.core.class_search_enhancer import SearchEnhancer
from mss.core.concrete_types.class_meta import Meta
from mss.core.helper_types.class_filesystem import Filesystem
from mss.core.simple_types.class_serializer import Serializer
from mss.core.simple_types.class_synonyms import Synonyms
from mss.core.simple_types.class_tags_on_demand import TagsOnDemand
from mss.core.simple_types.class_theme import Theme
from mss.core.simple_types.class_theme_statistics import ThemeStatistics


def load_all_themes(path: str, filesystem: Filesystem) -> List[Theme]:
    """Instantiate and return all available themes."""
    path = filesystem.absolute(path)
    names = filesystem.list_folders(path)
    themes = []

    for directory_name in names:
        theme = load_single_theme(path, directory_name, filesystem)
        if theme is not None:
            themes.append(theme)

    return themes


def load_single_theme(path: str, directory_name: str,
                      filesystem: Filesystem) -> Optional[Theme]:
    """Create instance for single theme."""
    theme_name = filesystem.join(path, directory_name, 'theme.yaml')
    uuids_name = filesystem.join(path, directory_name, 'used_uuids.csv')

    try:
        with open(theme_name, mode='r', encoding='utf-8') as file:
            theme_content = yaml.load(file, Loader=yaml.SafeLoader)
    except FileNotFoundError:
        return None

    used_uuids_content = filesystem.read_file(uuids_name)

    theme = Theme(
        name=theme_content['name'],
        directory=directory_name,
        synonyms=Synonyms.from_dict(
            theme_content.get('synonyms', {})
        ),
        tags_on_demand=TagsOnDemand.from_dict(
            theme_content.get('tags_on_demand', {})
        ),
        statistics=ThemeStatistics(),
        used_uuids={x.strip() for x in used_uuids_content.split('\n')},
    )

    return theme


def update_one_theme(theme: Theme, repository: Repository,
                     filesystem: Filesystem) -> None:
    """"""
    path = filesystem.join(filesystem.root_folder, theme.directory, 'metainfo')
    serializer = Serializer(target_type=Meta)
    enhancer = SearchEnhancer(synonyms=theme.synonyms)

    i = 0
    for filename in filesystem.list_files(path):
        # i += 1
        # if i > 10:
        #     break
        full_path = filesystem.join(path, filename)
        content = filesystem.read_file(full_path)
        record = json.loads(content)
        instance: Meta = serializer.from_source(**record)
        tags = enhancer.get_extended_tags(instance)
        repository.add_record(instance, tags)
        theme.statistics.add_item(
            item_date=instance.registered_on,
            item_size=instance.bytes_in_file,
            item_tags=instance.tags,
        )
        instance.theme_directory = theme.directory
