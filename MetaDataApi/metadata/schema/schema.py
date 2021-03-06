import graphene
from graphene_django.filter import DjangoFilterConnectionField
from MetaDataApi.metadata.schema import meta_schema, instances_schema


class Query(meta_schema.Query, instances_schema.Query):
    pass


class Mutation(meta_schema.Mutation, instances_schema.Mutation):
    pass
