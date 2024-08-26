from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from ..serializers import AuthorSerializer
from authors.permissions import IsOwner, NotAuthenticated
from rest_framework.decorators import action

class AuthorViewSet(ModelViewSet):
    '''
    Nesta view, sobreescrevi os métodos `get_queryset`, `get_permissions`, `partial_update` e `destroy` para garantir que os usuários só possam ver e manipular seus próprios dados.
    
    No metodo queryset, eu retorno apenas um usuário, que é o usuário autenticado.
   
    no metodo partial_update e destroy, em vez de usar intance = self.get_object(), eu uso instance = self.get_queryset().first() para obter o usuário autenticado. Porque o self.get_object() precisa passar um id na URL, e eu não quero que o usuário passe um id na URL, eu quero que ele acesse o seu próprio perfil.
    '''
    serializer_class = AuthorSerializer

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        """
        Retorna os dados do usuário autenticado.
        """
        obj = self.get_queryset().first()
        serializer = self.get_serializer(instance=obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        """
        Garante que os usuários só possam ver e manipular seus próprios dados.
        """
        User = get_user_model()
        return User.objects.filter(username=self.request.user.username) if self.request.user.is_authenticated else User.objects.none()

    def get_permissions(self):
        """
        Determina quais permissões são necessárias para acessar cada ação.
        """
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Permite acesso para usuários autenticados
        if self.request.method == 'POST':
            return [NotAuthenticated()]  # Permite registro público (apenas para novos usuários)
        if self.request.method in ['DELETE', 'PATCH']:
            return [IsOwner()]  # Permite acesso apenas ao proprietário do recurso (usuário)
        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs):
        """
        Atualiza parcialmente o usuário autenticado.
        """
        instance = self.get_queryset().first()  # Obtém a instância do usuário autenticado
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Deleta o usuário autenticado.
        """
        instance = self.get_queryset().first()  # Obtém a instância do usuário autenticado
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
