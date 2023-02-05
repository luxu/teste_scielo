from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

from core.models import Autor, Figura, Artigo
from xml_parser import (
    get_autores_from_xml,
    get_figuras_from_xml,
    get_artigos_from_xml
)


@pytest.fixture
def tree():
    arquivos = Path().cwd().parent.glob('**/*.xml')
    for file_name in arquivos:
        with open(file_name, encoding='utf-8') as fp:
            arquivo = ET.parse(fp)
    return arquivo


@pytest.fixture
def figura(db, tree):
    figuras = get_figuras_from_xml(tree)
    Figura.objects.bulk_create(
        Figura(
            rotulo=figura['rotulo'],
            legenda=figura['legenda'],
            imagem=figura['imagem']
        )
        for figura in figuras
    )
    return Figura.objects.get(id=1)


@pytest.fixture
def autor(db, tree):
    autores = [autor['nome'] for autor in get_autores_from_xml(tree)]
    Autor.objects.bulk_create(
        Autor(nome=autor)
        for autor in autores
    )
    return tuple(Autor.objects.filter(id=2).values_list())[0][1]


@pytest.fixture
def artigo(db, autor):
    artigo = Artigo.objects.create(
        titulo_do_periodico="Biosfera",
        titulo_do_artigo="",
        volume=0,
        numero=0,
        ano_de_publicacao=2023
    )
    artigo.autores.add(autor)
    return artigo



def test_save_autor(autor):
    assert autor == 'Alfredo Junior Paiola Albrecht'


def test_save_figura(figura):
    assert figura.imagem == \
           "https://minio.scielo.br/documentstore/1808-1657/NxWBM9hvfj4hgWbvB6GP8nF/ef0ac2c14618600e94bb76c8d2cf8155e3e270b8.tif"
    assert figura.rotulo == "Figure 1"
    assert figura.legenda == "Rainfall, minimum (min) and maximum (max) temperature, during the experiments. Maripá, PR, Brazil, 2020–2021."


def test_save_artigo(artigo):
    assert artigo is not None
    assert artigo.volume == 0
    assert len(artigo.to_dict()['autores']) == 1


def test_get_figuras_xml(tree):
    figuras = get_figuras_from_xml(tree)
    assert figuras[0]['id'] == 'f01'
    assert figuras[0]['imagem'] == \
           'https://minio.scielo.br/documentstore/1808-1657/NxWBM9hvfj4hgWbvB6GP8nF/ef0ac2c14618600e94bb76c8d2cf8155e3e270b8.tif'
    assert figuras[0]['legenda'] =='Rainfall, minimum (min) and maximum (max) temperature, during the ' \
                                   'experiments. Maripá, PR, Brazil, 2020–2021.'
    assert figuras[0]['rotulo'] == 'Figure 1'


def test_get_autores_xml(tree):
    autores = [autor['nome'] for autor in get_autores_from_xml(tree)]
    assert autores[0] == 'Leandro Paiola Albrecht'
    assert autores[1] == 'Alfredo Junior Paiola Albrecht'
    assert autores[2] == 'André Felipe Moreira Silva'
    assert autores[3] == 'Lucas Martins da Silva'
    assert autores[4] == 'Debora Cristine Neuberger'
    assert autores[5] == 'Gabriel Zanfrilli'
    assert autores[6] == 'Vagner Maurício da Silva Antunes'

def test_get_artigos_xml(tree):
    autores = [autor['nome'] for autor in get_autores_from_xml(tree)]
    artigos = get_artigos_from_xml(tree)
    figuras = get_figuras_from_xml(tree)
    assert artigos[0]['titulo_do_periodico'] == 'Arquivos do Instituto Biológico'
    assert artigos[0]['titulo_do_artigo'] == 'Sumatran fleabane ('
    assert artigos[0]['volume'] == '89'
    assert artigos[0]['numero'] == 0
    assert artigos[0]['ano_de_publicacao'] == '2023'
    assert artigos[0]['autores'] == autores
    assert artigos[0]['figuras'] == figuras
