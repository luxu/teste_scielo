# Generated by Django 4.1.5 on 2023-02-06 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_remove_artigo_autores_artigo_autores"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="artigo",
            name="autores",
        ),
        migrations.AddField(
            model_name="artigo",
            name="autores",
            field=models.ManyToManyField(related_name="artigos", to="core.autor"),
        ),
    ]
