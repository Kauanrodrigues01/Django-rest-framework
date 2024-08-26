from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    Está classe é uma permissão personalizada que verifica se o usuário é o autor de um recipe, se for ele pode editar, se não só pode ler
    
    # has_object_permission é chamado para verificar se o usuário tem permissão para acessar um objeto específico
    
    # has_permission é chamado para verificar se o usuário tem permissão para acessar a lista de objetos
    '''
    def has_object_permission(self, request, view, obj):
        '''
            Neste caso o obj é um objeto do tipo Recipe, que tem um campo author que é uma ForeignKey para User
        '''
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.author == request.user
    
    def has_permission(self, request, view):
        return super().has_permission(request, view)