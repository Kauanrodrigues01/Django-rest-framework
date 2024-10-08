from recipes.models import Recipe, Category
from django.contrib.auth.models import User
from tag.models import Tag
from rest_framework import serializers
from collections import defaultdict
from authors.validators import AuthorRecipeValidator # Validador de entrada de dados para o Recipe
from django.core.exceptions import ValidationError

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

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
        fields = ['id', 'title', 'description', 'slug', 'author', 'author_full_name', 'public', 'prepration', 'category','category_name', 'tags', 'tags_objects', 'tags_links', 'preparation_time', 'preparation_time_unit', 'servings', 'servings_unit', 'preparation_steps', 'cover']
    
    # Campos personalizados   
    author_full_name = serializers.CharField(max_length=255, read_only=True)
    public = serializers.BooleanField(
        source='is_published'
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
        view_name='recipes:tags-detail',
        read_only=True
    )
    
    def preparation_method(self, obj):
        '''
        Combina `preparation_time` e `preparation_time_unit` em uma string, indicando o tempo de preparo.
        '''
        if obj.preparation_time == 1:
            return f'{obj.preparation_time} {obj.preparation_time_unit[:-1]}' # O método `[:-1]` remove o último caractere da string.
        return f'{obj.preparation_time} {obj.preparation_time_unit}'
    
    def validate(self, dados):
        '''
        quando a view passa a instancia a gente tem acesso a ela usando self.instance
        '''
        # Se a instância existe e o campo 'servings' não for fornecido, Nos dados da atualização, ele paga o valor do servings da instância e atribui ao campo 'servings' dos dados.
        if self.instance is not None and dados.get('servings') is None:
            dados['servings'] = self.instance.servings
            
        if self.instance is not None and dados.get('preparation_time') is None:
            dados['preparation_time'] = self.instance.preparation_time
        
        super_validate = super().validate(dados)
        AuthorRecipeValidator(
            dados, 
            ErrorClass=serializers.ValidationError
        )
        return super_validate # Retorna os dados validados.