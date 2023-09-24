import graphene
from graphene_django import DjangoObjectType
from books.models import Book

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "description")
    
class createBookMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
    
    book = graphene.Field(BookType)

    def mutate(self, info, title, description):
        book = Book(title=title, description=description)
        book.save()
        return createBookMutation(book=book)
    
class deleteBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    book = graphene.Field(BookType)

    def mutate(self, info, id):
        book = Book.objects.get(pk=id)
        book.delete()
        return deleteBookMutation(book=book)
    
class updateBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String(default_value=None)
        description = graphene.String(default_value=None)
    
    book = graphene.Field(BookType)

    def mutate(self, info, id, title, description):
        book = Book.objects.get(pk=id)
        if title is not None:
            book.title = title
        if description is not None:
            book.description = description
        book.save()
        return updateBookMutation(book=book)

class Query(graphene.ObjectType):
    ping = graphene.String(default_value="Pong!")
    books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.ID())

    def resolve_books(self, info):
        return Book.objects.all()
    
    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)
    
class Mutation(graphene.ObjectType):
    create_book = createBookMutation.Field()
    delete_book = deleteBookMutation.Field()
    update_book = updateBookMutation.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)