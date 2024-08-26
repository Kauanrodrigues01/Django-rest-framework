from django.db.models.functions import Concat
from django.db.models import F, Value
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from recipes.models import Recipe
from tag.models import Tag
from ..serializers import RecipeSerializer, TagSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
# Permissions Prontas
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny, IsAdminUser
# Permissions Personalizadas
from ..permissions import IsOwnerOrReadOnly

class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100
    

class RecipeAPIv2ViewSet(ModelViewSet):
    '''
    **Métodos Importantes:**
    - `list` (GET): Obtém vários elementos.
    - `create` (POST): Cria um novo elemento.
    - `retrieve` (GET): Obtém um único elemento.
    - `update` (PUT): Atualiza um elemento.
    - `partial_update` (PATCH): Atualiza parcialmente um elemento.

    **Métodos Personalizados:**
    - `get_queryset()`: Retorna a queryset usada para listar os objetos. Pode ser personalizada para filtrar a queryset com base em parâmetros da Query String.
    - `get_object()`: Obtém um objeto específico da queryset, normalmente usado para recuperar um único objeto com base na ID passada na URL.
    - `partial_update()`: Atualiza parcialmente um objeto específico.

    **Outros Detalhes:**
    - `self.kwargs`: Contém os parâmetros passados na URL.
    - `self.request.query_params`: Contém os parâmetros da Query String passados após o ponto de interrogação na URL.
    
    **Limitando os metodos disponiveis:**
    - `http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']`: Limita os métodos HTTP disponíveis para a view.
    '''
    
    queryset = Recipe.objects.filter(is_published=True).annotate(
        author_full_name=Concat(
            F('author__first_name'), Value(' '),
            F('author__last_name'), Value(' ('),
            F('author__username'), Value(')'),
        )).order_by('-id').select_related('category', 'author').prefetch_related('tags')
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly,]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    
    def get_queryset(self):
        '''
        Este metodo é chamado toda vez que a view precisa de uma queryset, ele retorna a queryset que será usada para listar os objetos.
        
        Filtra a queryset com base nos parâmetros da Query String:
        - `category_id`: Filtra receitas por ID da categoria.
        - `author_id`: Filtra receitas por ID do autor.
        - `tags_ids`: Filtra receitas por IDs das tags.
        '''
        qs = super().get_queryset() # Pega a queryset definida na view
       
        category_id = self.request.query_params.get('category_id') # Pega o parametro category_id da Query String
        author_id = self.request.query_params.get('author_id') 
        tags_ids = self.request.query_params.getlist('tags_ids') 
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
    
    def get_object(self):
        '''
        self.kwargs.get('pk', '') -> Pega o valor da chave 'pk' nos parâmetros da URL, se não existir retorna uma string vazia.
        
        Verifica se o usuário tem permissão para acessar o objeto.
        '''
        pk = self.kwargs.get('pk', '')
        obj = get_object_or_404(self.get_queryset(), pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsOwnerOrReadOnly()]
        
        if self.request.method in ['POST']:
            return [IsAuthenticated()]
        
        if self.request.method in ['GET', 'OPTIONS', 'HEAD']:
            return [AllowAny()]
    
    def partial_update(self, request, *args, **kwargs):
        '''
        Atualiza parcialmente um objeto específico.
        O método `partial_update` é usado para modificar parcialmente os dados de um objeto.
        '''
        pk = kwargs.get('pk')
        
        recipe = self.get_object()
        serializer = RecipeSerializer(
            instance=recipe, 
            data=request.data, 
            partial=True, 
            many=False
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        # codigo adicional por mim para salvar o author
        request.data['author'] = request.user.id
        
        # codigo padrão da função create
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class TagAPIv2ViewSet(ModelViewSet):
    '''
    View para detalhes de tags. Permite recuperar e excluir tags.
    '''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'delete', 'patch']
    
    def get_permissions(self):
        """
        Define permissões com base no método HTTP da requisição.
        """
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]  # Somente admins podem alterar ou excluir tags
        if self.request.method == 'GET':
            return [AllowAny()]  # Todos podem visualizar tags
        return super().get_permissions()  # Permissões padrão para outros métodos
    
    def destroy(self, request, *args, **kwargs):
        """
        Exclui uma tag e retorna uma resposta.
        """
        tag = self.get_object()
        self.perform_destroy(tag)
        return Response({"detail": "Tag excluída com sucesso."}, status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        """
        Atualiza parcialmente uma tag e retorna uma resposta.
        """
        tag = self.get_object()
        serializer = self.get_serializer(tag, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    