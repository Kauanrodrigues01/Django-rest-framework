from django.db.models.functions import Concat
from django.db.models import F, Value
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from recipes.models import Recipe
from tag.models import Tag
from ..serializers import RecipeSerializer, TagSerializer
# from django.shortcuts import get_object_or_404
from rest_framework import status
# from rest_framework.views import APIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ValidationError

class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

class RecipeAPIv2ViewSet(ModelViewSet):
    '''
    Quando for personalizar metodos, tem que usar os nomes dos metodos que estão dentro dos mixins:
    - list(get varios elementos)
    - create(post)
    - retrieve(get unico elemento)
    - update(put)
    - partial_update(patch)
    '''
    queryset = Recipe.objects.filter(is_published=True).annotate(
        author_full_name=Concat(
            F('author__first_name'), Value(' '),
            F('author__last_name'), Value(' ('),
            F('author__username'), Value(')'),
        )).order_by('-id').select_related('category', 'author').prefetch_related('tags')
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    
    def get_queryset(self):
        '''
            # Os parametros da URL são passados como kwargs
            # Os parametros da Query String são passados como query_params
            # A diferença é que os parametros da URL são passados na URL e os parametros da Query String são passados na URL após o ponto de interrogação
        '''
        qs = super().get_queryset() # Pega a queryset definida na view
        print('Parametros da URL:', self.kwargs)
        print('Query String:', self.request.query_params)
       
        category_id = self.request.query_params.get('category_id', None) # Pega o parametro category_id da Query String e se não existir, retorna None
        author_id = self.request.query_params.get('author_id', None) # Pega o parametro author_id da Query String e se não existir, retorna None
        tags_ids = self.request.query_params.getlist('tags_ids') # Pega o parametro tags_ids da Query String e se não existir, retorna uma lista vazia
        if category_id is not None:
            if category_id.isdigit():
                qs = qs.filter(category_id=category_id)
            else:
                raise ValidationError('O parâmetro category_id deve ser um número inteiro.')
        if author_id is not None:
            if author_id.isdigit():
                qs = qs.filter(author_id=author_id)
            else:
                raise ValidationError('O parâmetro author_id deve ser um número inteiro.')
        if tags_ids:
            if all(tag_id.isdigit() for tag_id in tags_ids):
                qs = qs.filter(tags__id__in=tags_ids) # Acessa o relacionamento tags e filtra os elementos que tem o id na lista tags_ids, tags__id acessa o campo da tabela de tags e __in verifica se o valor está na lista
        else:
            raise ValidationError('Os parâmetros tags_ids devem ser números inteiros.')
        
        return qs
    
    def partial_update(self, request, *args, **kwargs):
        '''
        ## Kwargs é um dicionário que contém os argumentos passados para a view. Que são passados na URL.
        
        # queryset() é um método que retorna a queryset da view.
        '''
        pk = kwargs.get('pk')
        
        recipe = self.queryset.filter(pk=pk).first()
        serializer = RecipeSerializer(
            instance=recipe, 
            data=request.data, 
            partial=True, 
            many=False
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
 
class TagAPIv2Detail(RetrieveDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # Exemplos de métodos que podem ser sobrescritos(personalizados)
    # def get_queryset(self):
    #     user = self.request.user
    #     return Tag.objects.filter(created_by=user)

    def delete(self, request, *args, **kwargs):
        tag = self.get_object()
        self.perform_destroy(tag)
        return Response({"detail": "Tag excluída com sucesso."}, status=status.HTTP_204_NO_CONTENT)