# Generated by Django 4.1.5 on 2023-01-31 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_rename_autores_autor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="figura",
            name="imagem",
            field=models.CharField(max_length=200),
        ),
    ]
