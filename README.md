# MiniWorld API Mock

This is a graphQL API mock for MiniWorld.
Currently, only the distance API is mocked.

In future releases of MiniWorld, the `mobility part` is going to be completely decoupled from MiniWorld.
A distance matrix can be set `asynchronous` for each step. MiniWorld then uses the supplied distance matrix for the given `step`.
If a distance matrix is not yet supplied, MiniWorld is going to `wait` for it to be set.


## Install

### Create virtual environment
```python
mkvirtualenv -p python3.6 api_mock
```

### Install Python dependencies

```python
pip install -r requirements.txt
```


### Run GraphQL queries interactively

Run the API:

```bash
$ python mock.py
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

Go to http://127.0.0.1:5000/graphql, explore the documentation and execute queries and mutations.

#### Ping

```python
... from graphqlclient import GraphQLClient
... client = GraphQLClient('http://127.0.0.1:5000/graphql')
... client.execute('''
... query {
...   ping
... }
... ''')
'{"data":{"ping":"pong"}}'
```

#### Set Distance Matrix

```python
... from graphqlclient import GraphQLClient
... import json
... client = GraphQLClient('http://127.0.0.1:5000/graphql')

... res = client.execute('''
... mutation ($distance_matrix: String!) {
...     setDistanceMatrix(input: {distanceMatrix: $distance_matrix}) {
...         distanceMatrix
...         step
...     }
... }
...     ''', variables={'distance_matrix': '''
...     {
...         "0": {
...             "1": 10
...         },
...         "1": {
...             "2": 5
...         },
...         "2": {
...             "3": 2.5
...         }
...     }
...     '''})
... print(json.loads(res))
{'data': {'setDistanceMatrix': {'distanceMatrix': {'0': {'1': 10}, '1': {'2': 5}, '2': {'3': 2.5}}, 'step': 5}}}

... res = client.execute('''
... query {
...     distanceMatrix(step:0)
... }
...     ''')
... print(json.loads(res))
{'data': {'distanceMatrix': {'0': {'1': 10}, '1': {'2': 5}, '2': {'3': 2.5}}}}
```