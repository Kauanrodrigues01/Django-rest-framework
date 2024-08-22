from recipes.models import Recipe, Category
from django.contrib.auth.models import User
from tag.models import Tag
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class RecipeSerializer(serializers.ModelSerializer):
    '''
    # `source='is_published'`: Mapeia o campo `public` para o valor do campo `is_published` do modelo.
    
    # `SerializerMethodField`: Cria um campo personalizado no serializer que é preenchido pelo valor retornado de um método definido no serializer. O método responsável é chamado automaticamente durante a serialização e deve começar com "get_<nome_da_variavel>", no caso o nome do campo. Ele recebe o objeto que está sendo serializado e retorna o valor que será mostrado. Ou pode definir um nome especifico usando o argumento `method_name`.
    
    # `obj`: Refere-se a cada objeto que está sendo serializado. No caso, a cada objeto de Recipe, que é models que esta sendo serializado.
    
    # `PrimaryKeyRelatedField`: Representa um campo de relacionamento no serializer usando a chave primária do objeto relacionado. Nesse caso, o campo category representa a relação entre Recipe e Category através da chave primária (ID) da categoria.
    
    # `queryset=Category.objects.all()`: Define quais categorias estão disponíveis para a escolha. 
    
    # `StringRelatedField`: Este campo exibe a representação em string do objeto relacionado. No Django, isso se refere ao método `__str__` do modelo relacionado. Assim, ao usar `StringRelatedField`, o serializer retornará a string definida no método `__str__` do modelo `Category` em vez do ID da categoria.
    
    # `HyperlinkedRelatedField`: Este campo cria um link para o objeto relacionado. O argumento `view_name` define o nome da view que será usada para criar o link. Nesse caso, o link aponta para a view `recipes:recipes_api_v2_tag`, que é a view que exibe detalhes de uma tag específica. E quando for usar o HyperlinkedRelatedField, na view tem que passar o argumento `context={'request': request}` para o serializer, para que ele possa criar URLs absolutas para os objetos relacionados.
    '''
    # Campos do modelo Recipe
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'author', 'author_full_name', 'public', 'prepration', 'category_name', 'tags', 'tags_objects', 'tags_links']
    
    # Campos personalizados   
    author_full_name = serializers.CharField(max_length=255)
    public = serializers.BooleanField(
        source='is_published', 
        read_only=True
    )
    prepration = serializers.SerializerMethodField(
        method_name='preparation_method', 
        read_only=True
    )
    category_name = serializers.StringRelatedField(
        source='category',
        read_only=True
    )
    tags_objects = TagSerializer(
        source='tags', 
        many=True,
        read_only=True
    )
    tags_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        # queryset=Tag.objects.all(), # O queryset não é necessário, porque o campo é somente leitura.
        view_name='recipes:recipes_api_v2_tag',
        read_only=True
    )
    
    def preparation_method(self, obj):
        '''
        Combina `preparation_time` e `preparation_time_unit` em uma string, indicando o tempo de preparo.
        '''
        if obj.preparation_time == 1:
            return f'{obj.preparation_time} {obj.preparation_time_unit[:-1]}' # O método `[:-1]` remove o último caractere da string.
        return f'{obj.preparation_time} {obj.preparation_time_unit}'
