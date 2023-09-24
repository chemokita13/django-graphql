import graphene

class Query(graphene.ObjectType):
    ping = graphene.String(default_value="Pong!")

schema = graphene.Schema(query=Query)