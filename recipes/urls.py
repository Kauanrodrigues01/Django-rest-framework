from django.urls import path, include
from rest_framework.routers import SimpleRouter
from recipes import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

app_name = 'recipes'

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register(
    'recipes/api/v2',
    views.api.RecipeAPIv2ViewSet,
    basename='recipes-api'
)
recipe_api_v2_router.register(
    'recipes/api/v2/tag',
    views.api.TagAPIv2ViewSet,  # Registra o viewset de tags
    basename='tags'
)

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
    
    # Incluir as rotas do SimpleRouter
    path('', include(recipe_api_v2_router.urls)),
]
