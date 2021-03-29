# -*- coding: utf-8 -*-

"""Non user friendly script.
"""
from typing import List


def record_sorter(raw_record: dict) -> tuple:
    """Create tuple on which we could sort."""
    return (
        raw_record['series'],
        raw_record['sub_series'],
        raw_record['ordering'],
    )


def sort_json_records_inplace(records: List[dict]) -> None:
    """Perform sorting on list of json records."""
    records.sort(key=record_sorter)


def tie_json_records_inplace(records: List[dict]) -> None:
    """Mark list of records as group."""
    uuids = [x['uuid'] for x in records]

    for i in range(len(records)):
        content = records[i]
        assert content['uuid'] == uuids[i]

        content['group_members'] = uuids

        if i == 0:
            content['previous_record'] = ''
            content['next_record'] = uuids[1]

        elif i == len(records) - 1:
            content['previous_record'] = uuids[-2]
            content['next_record'] = ''

        else:
            content['previous_record'] = uuids[i - 1]
            content['next_record'] = uuids[i + 1]
