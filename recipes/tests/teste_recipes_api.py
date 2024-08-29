from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from django.urls import reverse
# o reverse é uma função que retorna a URL de uma view a partir do nome da URL

class RecipeAPIv2Test(test.APITestCase, RecipeMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        '''
        O reverse é uma função que retorna a URL de uma view a partir do nome da URL definida no arquivo de urls.py.
        
        # self.client.get(api_url) faz uma requisição GET para a URL retornada por reverse('recipes:recipe-api-list').
        
        # self.assertEqual(response.status_code, 200) verifica se o código de status da resposta é 200.
        '''
        api_url = reverse('recipes:recipe-api-list')
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, 200)
        
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        '''
        # self.make_recipe() cria uma receita.
        
        # self.client.get(api_url) faz uma requisição GET para a URL retornada por reverse('recipes:recipe-api-list').
        
        # response.data['count'] é o número de receitas retornadas pela API.
        
        # self.assertEqual(response.data['count'], 1) verifica se a API retornou uma receita.
        '''
        wanted_recipes = 7
        response = self.client.get(reverse('recipes:recipe-api-list'))
        print(response.data)