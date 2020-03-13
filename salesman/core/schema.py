import graphene

from salesman.conf import app_settings


class Price(graphene.String):
    """
    Price type used to display a formated price in graphql.
    """

    def __init__(self, *args, **kwargs):
        kwargs['resolver'] = self.price_resolver
        super().__init__(*args, **kwargs)

    @staticmethod
    def price_resolver(parent, info):

        if isinstance(parent, dict):
            # Price is already formated, return it.
            return parent[info.field_name]

        value = getattr(parent, info.field_name)
        context = {'request': info.context}
        return app_settings.SALESMAN_PRICE_FORMATTER(value, context=context)
