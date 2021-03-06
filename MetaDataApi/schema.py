import MetaDataApi.metadata.schema
import MetaDataApi.users.schema
import MetaDataApi.datapoints.schema
import MetaDataApi.dataproviders.schema


import graphene
import graphql_jwt


from graphene_django.debug import DjangoDebug


class Query(
        MetaDataApi.users.schema.Query,
        MetaDataApi.metadata.schema.schema.Query,
        # MetaDataApi.datapoints.schema.Query,
        MetaDataApi.dataproviders.schema.Query,
        graphene.ObjectType):

    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(
        MetaDataApi.users.schema.Mutation,
        MetaDataApi.metadata.schema.schema.Mutation,
        # MetaDataApi.datapoints.schema.Mutation,
        MetaDataApi.dataproviders.schema.Mutation,
        graphene.ObjectType):

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query, mutation=Mutation)
