# -*- coding: utf-8 -*-

"""Work with actual files using Filesystem class.
"""
import operator
from functools import reduce, partial
from itertools import chain
from typing import List, Optional

from mss import core
from mss.utils.utils_scripts import perc


def update_repositories(themes_repository: core.ThemesRepository,
                        repository: core.Repository,
                        root_path: str,
                        filesystem: core.Filesystem) -> None:
    """Put all meta info into repositories."""
    themes = load_all_themes(root_path, filesystem)

    for theme in themes:
        update_one_theme(root_path, theme, repository, filesystem)
        themes_repository.add(theme)

    default = make_default_theme(themes)
    themes_repository.add(default)


def load_all_themes(path: str,
                    filesystem: core.Filesystem) -> List[core.Theme]:
    """Instantiate and return all available themes."""
    path = filesystem.absolute(path)
    themes = []

    for directory_name in filesystem.list_folders(path):
        theme = load_single_theme(path, directory_name, filesystem)

        if theme is not None:
            themes.append(theme)

    return themes


def make_default_theme(themes: List[core.Theme]) -> core.Theme:
    """Make combined theme called "All themes"."""
    assert themes
    _sum = partial(reduce, operator.add)
    all_uuids = set(chain.from_iterable(x.used_uuids for x in themes))

    return core.Theme(
        name='All themes',
        directory='all_themes',
        synonyms=_sum(x.synonyms for x in themes),
        tags_on_demand=_sum(x.tags_on_demand for x in themes),
        statistics=_sum(x.statistics for x in themes),
        used_uuids=all_uuids,
    )


def load_single_theme(path: str, directory_name: str,
                      filesystem: core.Filesystem) -> Optional[core.Theme]:
    """Create instance for single theme."""
    theme_name = filesystem.join(path, directory_name, 'theme.yaml')
    uuids_name = filesystem.join(path, directory_name, 'used_uuids.csv')

    try:
        theme_content = filesystem.read_yaml(theme_name)
    except FileNotFoundError:
        return None

    used_uuids_content = filesystem.read_file(uuids_name)

    theme = core.Theme(
        name=theme_content['name'],
        directory=directory_name,
        synonyms=core.Synonyms.from_dict(
            theme_content.get('synonyms', {})
        ),
        tags_on_demand=core.TagsOnDemand.from_dict(
            theme_content.get('tags_on_demand', {})
        ),
        statistics=core.ThemeStatistics(),
        used_uuids={x.strip() for x in used_uuids_content.split('\n')},
    )

    return theme


def update_one_theme(root: str, theme: core.Theme, repository: core.Repository,
                     filesystem: core.Filesystem) -> None:
    """Update contents of a single theme."""
    path = filesystem.join(root, theme.directory, 'metainfo')
    enhancer = core.SearchEnhancer(synonyms=theme.synonyms)

    print('Updating:', theme.name)
    for filename in perc(filesystem.list_files(path)):
        full_path = filesystem.join(path, filename)
        content = filesystem.read_json(full_path)

        for record in content.values():
            instance = core.Meta(directory=theme.directory, **record)
            tags = enhancer.get_extended_tags_with_synonyms(instance)
            repository.add(instance, tags)
            theme.statistics.add(item_date=instance.registered_on,
                                 item_size=instance.bytes_in_file,
                                 item_tags=instance.tags)
