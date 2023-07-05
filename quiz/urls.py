from django.urls import path
from graphene_django.views import GraphQLView
from .schema import schema
# from django.contrib import admin


urlpatterns = [
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema))
    # path("admin")
]