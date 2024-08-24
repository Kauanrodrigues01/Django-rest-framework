from django.urls import path, include

from recipes import views
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
app_name = 'recipes'

'''
# No caso o simpleRouter cria DUAS ROTAS:

# recipes:recipes-api-list -> recipes/api/v2/ -> Mostra todos os elementos

# recipes:recipes-api-detail -> recipes/api/v2/<int:pk>/ -> Mostra um elemento especifico
'''
recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register(
    'recipes/api/v2',
    views.api.RecipeAPIv2ViewSet,
    basename='recipes-api' # Muda o nome base da rotas list e detail
)
print(recipe_api_v2_router.urls) # Aqui dá para ver as rotas criadas

urlpatterns = [
    path(
        '',
        views.site.RecipeListViewHome.as_view(),
        name="home"
    ),
    path(
        'recipes/search/',
        views.site.RecipeListViewSearch.as_view(),
        name="search"
    ),
    path(
        'recipes/tags/<slug:slug>/',
        views.site.RecipeListViewTag.as_view(),
        name="tag"
    ),
    path(
        'recipes/category/<int:category_id>/',
        views.site.RecipeListViewCategory.as_view(),
        name="category"
    ),
    path(
        'recipes/<int:pk>/',
        views.site.RecipeDetail.as_view(),
        name="recipe"
    ),
    path(
        'recipes/api/v1/',
        views.site.RecipeListViewHomeApi.as_view(),
        name="recipes_api_v1",
    ),
    path(
        'recipes/api/v1/<int:pk>/',
        views.site.RecipeDetailAPI.as_view(),
        name="recipes_api_v1_detail",
    ),
    path(
        'recipes/theory/',
        views.site.theory,
        name='theory',
    ),
    
    # Django REST Framework
    path(
        'recipes/api/token/', 
        TokenObtainPairView.as_view(), 
        name='token_obtain_pair'
    ),
    path(
        'recipes/api/token/refresh/', 
        TokenRefreshView.as_view(), 
        name='token_refresh'
    ),
    path(
        'recipes/api/token/verify/', 
        TokenVerifyView.as_view(), 
        name='token_verify'
    ),
    
    # Por ultimo
    path(
        'recipes/api/v2/tag/<int:pk>/',
        views.api.TagAPIv2Detail.as_view(),
        name='recipes_api_v2_tag',
    ),
    path('', include(recipe_api_v2_router.urls)),
]