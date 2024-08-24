from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeValidator:
    def __init__(self, dados, erros=None, ErrorClass=None):
        self.errors = defaultdict(list) if erros is None else erros
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.dados = dados
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_servings()
        self.clean_preparation_time()
        
        cd = self.dados

        title = cd.get('title')
        description = cd.get('description')

        if title == description:
            self.errors['title'].append('Cannot be equal to description')
            self.errors['description'].append('Cannot be equal to title')

        if self.errors:
            raise self.ErrorClass(self.errors)


    def clean_title(self):
        title = self.dados.get('title')

        if len(title) < 5:
            self.errors['title'].append('Must have at least 5 chars.')


    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.dados.get(field_name)

        if not is_positive_number(field_value):
            self.errors[field_name].append('Must be a positive number')

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.dados.get(field_name)

        if not is_positive_number(field_value):
            self.errors[field_name].append('Must be a positive number')
