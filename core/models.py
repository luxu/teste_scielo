from django.db import models


class Artigo(models.Model):
    titulo_do_periodico = models.CharField(
        max_length=100
    )
    titulo_do_artigo = models.CharField(
        max_length=100
    )
    volume = models.IntegerField()
    numero = models.IntegerField()
    ano_de_publicacao = models.IntegerField()
    autores = models.ManyToManyField(
        'Autor',
        related_name='artigos'
    )

    def __str__(self):
        return self.titulo_do_periodico

    def to_dict(self):
        return {
            'id': self.id,
            'titulo_do_periodico': self.titulo_do_periodico,
            'titulo_do_artigo': self.titulo_do_artigo,
            'volume': self.volume,
            'numero': self.numero,
            'ano_de_publicacao': self.ano_de_publicacao,
            'autores': list(self.autores.values_list('id', flat=True))
        }


class Figura(models.Model):
    rotulo = models.CharField(
        max_length=50
    )
    legenda = models.CharField(
        max_length=50
    )
    imagem = models.CharField(
        max_length=200
    )

    def __str__(self):
        return self.rotulo


class Autor(models.Model):
    nome = models.CharField(
        max_length=50
    )

    def __str__(self):
        return self.nome
