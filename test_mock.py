import json

import pytest
from graphene.test import Client
from graphql import GraphQLError

from mock import schema


@pytest.fixture
def client():
    client = Client(schema)
    old_execute = client.execute

    def new_execute(*args, **kwargs):
        res = old_execute(*args, **kwargs)
        if res.get('errors') is not None:
            raise GraphQLError(res['errors'])

        print(json.dumps(res['data'], indent=2))

        return res

    client.execute = new_execute
    return client


def test_set_distance_matrix(client, snapshot):
    res = client.execute('''
mutation ($distance_matrix: String!) {
    setDistanceMatrix(input: {clientMutationId: "abc", distanceMatrix: $distance_matrix}) {
        distanceMatrix
        step
    }
}
    ''', variable_values={'distance_matrix': '''
    {
        "0": {
            "1": 10
        },
        "1": {
            "2": 5
        },
        "2": {
            "3": 2.5
        }
    }
    '''})
    snapshot.assert_match(res)


def test_get_distance_matrix(client, snapshot):
    client.execute('''
    mutation ($distance_matrix: String!) {
        setDistanceMatrix(input: {clientMutationId: "abc", distanceMatrix: $distance_matrix}) {
            distanceMatrix
            step
        }
    }
        ''', variable_values={'distance_matrix': '''
        {
            "0": {
                "1": 10
            },
            "1": {
                "2": 5
            },
            "2": {
                "3": 2.5
            }
        }
        '''})
    res = client.execute('''
query {
    distanceMatrix(step:0)
}
    ''')
    snapshot.assert_match(res)
