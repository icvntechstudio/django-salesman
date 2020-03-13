import graphene

from .basket.schema import Query as BasketQuery

from .basket.schema import Mutation as BasketMutation


class Query(BasketQuery, graphene.ObjectType):
    """
    Root graphql query for Salesman.
    """


class Mutation(BasketMutation, graphene.ObjectType):
    """
    Root grapql mutations for Salesman.
    """


schema = graphene.Schema(query=Query, mutation=Mutation)
