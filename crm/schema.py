import graphene


class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    message = graphene.String()

    def mutate(self, info, name):
        return CreateCustomer(message=f"Customer {name} created!")

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello from CRM schema!")