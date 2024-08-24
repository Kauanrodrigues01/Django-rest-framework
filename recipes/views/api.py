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
    
    def partial_update(self, request, *args, **kwargs):
        '''
        ## Kwargs é um dicionário que contém os argumentos passados para a view. Que são passados na URL.
        
        # queryset() é um método que retorna a queryset da view.
        '''
        pk = kwargs.get('pk')
        
        recipe = self.queryset().filter(pk=pk).first()
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