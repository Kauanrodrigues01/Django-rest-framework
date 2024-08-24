from django.urls import path

from recipes import views
from rest_framework.routers import SimpleRouter
app_name = 'recipes'

# Tem sempre uma / no final das urls, para mudar isso, coloca o parametro `trailing_slash=False` na instancia do SimpleRouter
recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register(
    'recipes/api/v2',
    views.api.RecipeAPIv2ViewSet,
    basename='tag'
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
        'recipes/api/v2/',
        views.api.RecipeAPIv2ViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }), # chamando class based view
        name='recipes_api_v2',
    ),
    path(
        'recipes/api/v2/<int:pk>/',
        views.api.RecipeAPIv2ViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='recipes_api_v2_detail',
    ),
    path(
        'recipes/api/v2/tag/<int:pk>/',
        views.api.TagAPIv2Detail.as_view(),
        name='recipes_api_v2_tag',
    ),
]
