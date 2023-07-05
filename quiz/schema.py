import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Quizzes, Category, Question, Answer


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id","name")

class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id","title","category", "quiz")

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title", "quiz")

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question","answer_text")

class Query(graphene.ObjectType):

    # all_quizzes = graphene.Field(QuizzesType, id = graphene.Int())
    all_question = graphene.Field(QuestionType, id = graphene.Int())
    all_answers = graphene.List(AnswerType, id = graphene.Int())
    
    def resolve_all_question(root, info, id):
        return Question.objects.get(pk=id)

    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)

class CategoryMutation(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)   
        category.save()
        return CategoryMutation(category=category)

class QuizzesMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)

    quizzes = graphene.Field(QuizzesType)

    @classmethod
    def mutate(cls, root, info, title):
        quizzes = Quizzes(title=title)
        quizzes.save()
        return QuizzesMutation(quizzes=quizzes)


class CategoryUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    categUpdate = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id, name):
        categUpdate = Category.objects.get(id=id)
        categUpdate.name = name
        categUpdate.save()
        return CategoryUpdateMutation(categUpdate)
    
# delete category of a particualr id
class CategoryDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    categDel = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        categDel = Category.objects.get(id=id)
        categDel.delete()
        return CategoryDeleteMutation(categDel)

class Mutation(graphene.ObjectType):
    add_category = CategoryMutation.Field()
    add_quizzes = QuizzesMutation.Field()
    update_category = CategoryUpdateMutation.Field()
    delete_category = CategoryDeleteMutation.Field()
    
    
schema = graphene.Schema(query=Query, mutation=Mutation)

