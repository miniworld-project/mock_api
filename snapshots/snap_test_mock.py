# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_get_distance_matrix 1'] = {
    'data': {
        'distanceMatrix': {
            '0': {
                '1': 10
            },
            '1': {
                '2': 5
            },
            '2': {
                '3': 2.5
            }
        }
    }
}

snapshots['test_set_distance_matrix 1'] = {
    'data': {
        'setDistanceMatrix': {
            'distanceMatrix': {
                '0': {
                    '1': 10
                },
                '1': {
                    '2': 5
                },
                '2': {
                    '3': 2.5
                }
            },
            'step': 0
        }
    }
}
