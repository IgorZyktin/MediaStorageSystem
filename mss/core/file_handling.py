# -*- coding: utf-8 -*-

"""Work with actual files using Filesystem class.
"""
import json
import operator
from functools import reduce, partial
from itertools import chain
from typing import List, Optional

import yaml

from mss.core.concrete_types.class_meta import Meta
from mss.core.concrete_types.class_repository import Repository
from mss.core.helper_types.class_filesystem import Filesystem
from mss.core.helper_types.class_search_enhancer import SearchEnhancer
from mss.core.simple_types.class_serializer import Serializer
from mss.core.simple_types.class_synonyms import Synonyms
from mss.core.simple_types.class_tags_on_demand import TagsOnDemand
from mss.core.simple_types.class_theme import Theme
from mss.core.simple_types.class_theme_repository import ThemeRepository
from mss.core.simple_types.class_theme_statistics import ThemeStatistics
from mss.utils.utils_scripts import perc


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


def make_default_theme(themes: List[Theme]) -> Theme:
    """Make combined theme called "All themes"."""
    assert themes
    _sum = partial(reduce, operator.add)
    all_uuids = set(chain.from_iterable(x.used_uuids for x in themes))

    return Theme(
        name='All themes',
        directory='all_themes',
        synonyms=_sum(x.synonyms for x in themes),
        tags_on_demand=_sum(x.tags_on_demand for x in themes),
        statistics=_sum(x.statistics for x in themes),
        used_uuids=all_uuids,
    )


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


def update_one_theme(root: str, theme: Theme, repository: Repository,
                     filesystem: Filesystem) -> None:
    """"""
    path = filesystem.join(root, theme.directory, 'metainfo')
    serializer = Serializer(target_type=Meta)
    enhancer = SearchEnhancer(synonyms=theme.synonyms)

    print('Updating:', theme.name)
    for filename in perc(filesystem.list_files(path)):
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
        instance.directory = theme.directory


def update_repositories(theme_repository: ThemeRepository,
                        repository: Repository,
                        root_path: str, filesystem: Filesystem) -> None:
    """Put all meta info into repositories."""
    themes = load_all_themes(root_path, filesystem)

    for _theme in themes:
        update_one_theme(root_path, _theme, repository, filesystem)
        theme_repository.add(_theme)

    default = make_default_theme(themes)
    theme_repository.add(default)
