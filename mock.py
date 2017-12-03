import json

import graphene
from flask import Flask
from flask_graphql import GraphQLView

distances = {}
step = 0


class DictScalar(graphene.Scalar):
    @staticmethod
    def serialize(x):
        return x


class PingQuery(graphene.ObjectType):
    ping = graphene.String()

    def resolve_ping(self, args):
        return 'pong'


class DistanceMatrixMutation(graphene.relay.ClientIDMutation):
    class Input:
        distance_matrix = graphene.String(required=True)

    distance_matrix = graphene.Field(DictScalar)
    step = graphene.Int()

    @classmethod
    def mutate_and_get_payload(cls, root, info, distance_matrix, client_mutation_id=None):
        global step
        distances[step] = json.loads(distance_matrix)
        step += 1
        return DistanceMatrixMutation(distance_matrix=distances[step - 1], step=step - 1)


class QueryDistanceMatrix(graphene.ObjectType):
    distance_matrix = graphene.Field(DictScalar, step=graphene.Int())

    def resolve_distance_matrix(self, info, step: int = 0):
        distance_matrix = distances.get(step)
        return distance_matrix


class Mutations(graphene.ObjectType):
    set_distance_matrix = DistanceMatrixMutation.Field()


class Query(PingQuery, QueryDistanceMatrix):
    node = graphene.relay.Node.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
app = Flask(__name__)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


def main():
    app.run(host="0.0.0.0")


if __name__ == '__main__':
    main()
