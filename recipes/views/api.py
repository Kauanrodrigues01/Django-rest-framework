from django.db.models.functions import Concat
from django.db.models import F, Value
from rest_framework.response import Response

from rest_framework.decorators import api_view
from recipes.models import Recipe
from tag.models import Tag
from ..serializers import RecipeSerializer, TagSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status


@api_view(['GET'])
def recipe_api_list(request):
    '''
    # `author_full_name` é um campo virtual criado ao concatenar os campos `author__first_name`, `author__last_name`, e `author__username` do modelo `Recipe`. Isso permite acessá-lo como um campo normal do modelo.

    # Os `__` (dois underlines) são usados para acessar campos relacionados. Como `author` é uma chave estrangeira para o modelo `User`, `author__first_name` permite acessar o campo `first_name` do modelo `User` a partir do modelo `Recipe`.
    
    # `many=True`: Indica que estamos serializando vários objetos
    
    # `select_related('category', 'author')`: O método `select_related` é usado para carregar os objetos relacionados ao mesmo tempo que os objetos principais. Isso evita consultas adicionais ao banco de dados para carregar os objetos relacionados. Nesse caso, `category` e `author` são carregados ao mesmo tempo que os objetos `Recipe`. É útil quando você tem um relacionamento "foreign key" ou "one-to-one". 
    ● Resumindo ele pega o Recipe, Category e Author em uma única consulta e passa para o serializer. Deixando o codigo mais rápido e eficiente.
    
    # `prefetch_related('tags')`: O método `prefetch_related` é usado para carregar objetos relacionados em uma consulta separada. Isso é útil quando você precisa carregar objetos relacionados que são muitos para muitos. Nesse caso, `tags` é carregado em uma consulta separada dos objetos `Recipe`. É útil para relacionamentos "many-to-many" ou "reverse foreign key"
    
    # `context={'request': request}`: Passa o objeto `request` para o serializer. Isso é útil para serializar campos que dependem do objeto `request`, como URLs absolutas. Como o HyperlinkedRelatedField, que usa o objeto `request` para criar URLs absolutas para os objetos relacionados.
    '''
    recipes = Recipe.objects.filter(is_published=True).annotate(
        author_full_name=Concat(
            F('author__first_name'), Value(' '),
            F('author__last_name'), Value(' ('),
            F('author__username'), Value(')'))).order_by('-id').select_related('category', 'author').prefetch_related('tags')[:10]
    
    serializer = RecipeSerializer(instance=recipes, many=True, context={'request': request}) 

    return Response(serializer.data)

@api_view(['GET', 'DELETE'])
def recipe_api_detail(request, pk):
    '''
    # `get_object_or_404` busca um objeto `Recipe` com a chave primária (`pk`) correspondente. Se o objeto não for encontrado, retorna um erro 404. Isso é melhor do que `filter(pk=pk)`, que poderia retornar um objeto vazio e causar erros no código.

    # `author_full_name` é criado da mesma forma que na função `recipe_api_list`.
    
    # `many=False`: Indica que estamos serializando um único objeto.
    '''
    recipe = get_object_or_404(
        Recipe.objects.filter(is_published=True).annotate(
        author_full_name=Concat(
            F('author__first_name'), Value(' '),
            F('author__last_name'), Value(' ('),
            F('author__username'), Value(')'))).select_related('category', 'author').prefetch_related('tags'), 
        pk=pk)
    
    serializer = RecipeSerializer(instance=recipe, many=False, context={'request': request}) 

    return Response(serializer.data)

@api_view(['GET'])
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.all(), pk=pk)
    serializer = TagSerializer(instance=tag, many=False)
    return Response(serializer.data)
