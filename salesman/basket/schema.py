import graphene
from graphene_django import DjangoObjectType

from salesman.core.schema import Price
from .models import Basket, BasketItem
from .serializers import ExtraRowsField, BasketItemCreateSerializer


class ExtraRowType(graphene.ObjectType):
    label = graphene.String(default_value="")
    amount = Price(default_value=0)
    extra = graphene.JSONString(default_value="{}")


class ExtraRows(graphene.List):
    """
    Extra rows field used to display `extra_rows` on both the
    basket and basket item type.
    """

    def __init__(self, *args, **kwargs):
        kwargs['resolver'] = self.extra_rows_resolver
        super().__init__(ExtraRowType, *args, **kwargs)

    @staticmethod
    def extra_rows_resolver(parent, info):
        extra_rows = getattr(parent, 'extra_rows')
        return ExtraRowsField().to_representation(extra_rows)


class BasketItemType(DjangoObjectType):
    class Meta:
        model = BasketItem


class BasketType(DjangoObjectType):
    items = graphene.List(BasketItemType, source='get_items')
    subtotal = Price()
    total = Price()
    extra = graphene.JSONString()
    extra_rows = ExtraRows()

    class Meta:
        model = Basket


class BasketItemCreateMutation(graphene.Mutation):
    class Input:
        ref = graphene.String()
        product_type = graphene.String(required=True)
        product_id = graphene.Int(required=True)
        quantity = graphene.Int()
        extra = graphene.JSONString()

    basket = graphene.Field(BasketType)
    item = graphene.Field(BasketItemType)

    @staticmethod
    def mutate(parent, info, **kwargs):
        basket, _ = Basket.objects.get_or_create_from_request(info.context)
        basket.update(info.context)
        context = {'request': info.context, 'basket': basket}
        serializer = BasketItemCreateSerializer(data=kwargs, context=context)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return BasketItemCreateMutation(basket=basket, item=item)


class Query:
    basket = graphene.Field(BasketType)

    @staticmethod
    def resolve_basket(parent, info, **kwargs):
        basket, _ = Basket.objects.get_or_create_from_request(info.context)
        basket.update(info.context)
        return basket


class Mutation:
    basket_item_create = BasketItemCreateMutation.Field()
