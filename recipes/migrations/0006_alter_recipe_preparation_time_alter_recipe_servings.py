# Generated by Django 4.2 on 2024-08-24 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_recipe_options_alter_recipe_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='preparation_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='servings',
            field=models.IntegerField(default=1),
        ),
    ]