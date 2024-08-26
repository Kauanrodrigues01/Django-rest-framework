from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Permissão personalizada que permite o acesso apenas ao proprietário do objeto. No caso um usuario só pode acessar o seu próprio perfil.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj == request.user

    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
class NotAuthenticated(BasePermission):
    """
    Permissão personalizada que permite o acesso apenas se o usuário não estiver autenticado.
    """
    
    def has_permission(self, request, view):
        # Permite acesso apenas se o usuário não estiver autenticado
        return not request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
