from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class AuthorSerializer(serializers.ModelSerializer):
    # Campo de senha, configurado para ser escrito mas não exibido, e validado com regras padrão de senhas
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], read_only=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'username': {'required': True},  # Define o campo 'username' como obrigatório
            'email': {'required': True},  # Define o campo 'email' como obrigatório
            'first_name': {'required': True},  # Define o campo 'first_name' como obrigatório
            'last_name': {'required': True},  # Define o campo 'last_name' como obrigatório
        }

    def validate(self, attrs):
        """ 
        Valida os dados antes de criar ou atualizar um usuário.
        """
        User = get_user_model()
        nomes_nao_permitidos = ['admin', 'root', 'administrator']

        if self.instance:
            # Se o usuário já existe (ou seja, uma instância foi passada), os valores existentes são usados se não forem fornecidos novos valores
            attrs['username'] = attrs.get('username', self.instance.username)
            attrs['email'] = attrs.get('email', self.instance.email)
            attrs['first_name'] = attrs.get('first_name', self.instance.first_name)
            attrs['last_name'] = attrs.get('last_name', self.instance.last_name)

        # Verifica se o username ou email já existem, excluindo o usuário atual
        if User.objects.filter(username=attrs['username']).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('Username already exists')
        if User.objects.filter(email=attrs['email']).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('Email already exists')

        # Validações adicionais
        if attrs['username'] in nomes_nao_permitidos:
            raise serializers.ValidationError('Username not allowed')
        if attrs['username'].isdigit():
            raise serializers.ValidationError('Username cannot be only numbers')
        if attrs['first_name'].isdigit():
            raise serializers.ValidationError('First name cannot be only numbers')
        if attrs['last_name'].isdigit():
            raise serializers.ValidationError('Last name cannot be only numbers')

        return attrs

    def create(self, validated_data):
        """
        Cria um novo usuário com os dados validados.
        Este método é chamado quando o serializer **NÃO** recebe uma instância (`instance=None`).
        """
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """
        Atualiza os dados de um usuário existente.
        Este método é chamado quando o serializer **RECEBE** uma instância existente (ou seja, `instance` é fornecido).
        """
        instance.username = validated_data.get('username', instance.username) # pegar o valor de 'username' de validated_data, se não existir, pegar o valor de instance.username
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Remove a senha da representação do usuário quando os dados são serializados para resposta.
        """
        representation = super().to_representation(instance)
        representation.pop('password', None)  # Remove a senha da representação, se não existir, não faz nada
        return representation
