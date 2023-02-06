import os
import xml.etree.ElementTree as ET
from pathlib import Path
from http import HTTPStatus
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from xml_parser import (
    get_autores_from_xml,
    get_figuras_from_xml,
    get_artigos_from_xml
)
from .models import Figura, Autor, Artigo

DEFAULT_PAGE_SIZE = 25

def listar_figuras(request):
    template_name = 'core/index.html'
    figuras = Figura.objects.all()
    context = {
        'figuras': figuras
    }
    return render(request, template_name, context)

def criar_figuras(request):
    template_name = 'core/confirmar_figuras.html'
    arquivos = Path().cwd().parent.glob('**/*.xml')
    for file_name in arquivos:
        with open(file_name, encoding='utf-8') as fp:
            tree = ET.parse(fp)
    figuras = get_figuras_from_xml(tree)
    Figura.objects.bulk_create(
        Figura(
            rotulo=figura['rotulo'],
            legenda=figura['legenda'],
            imagem=figura['imagem']
        )
        for figura in figuras
    )
    return render(request, template_name)

def listar_autores(request):
    template_name = 'core/listar_autores.html'
    autores = Autor.objects.all()
    context = {
        'autores': autores
    }
    return render(request, template_name, context)


def criar_autores(request):
    template_name = 'core/confirmar_autores.html'
    arquivos = Path().cwd().parent.glob('**/*.xml')
    for file_name in arquivos:
        with open(file_name, encoding='utf-8') as fp:
            tree = ET.parse(fp)
    autores = [autor['nome'] for autor in get_autores_from_xml(tree)]
    Autor.objects.bulk_create(
        Autor(nome=autor)
        for autor in autores
    )
    return render(request, template_name)

def listar_artigos(request):
    template_name = 'core/listar_artigos.html'
    artigos = Artigo.objects.all()
    context = {
        'artigos': artigos
    }
    return render(request, template_name, context)


def criar_artigos(request):
    template_name = 'core/confirmar_artigos.html'
    arquivos = Path().cwd().parent.glob('**/*.xml')
    for file_name in arquivos:
        with open(file_name, encoding='utf-8') as fp:
            tree = ET.parse(fp)
        artigos = list(get_artigos_from_xml(tree))
        Artigo.objects.bulk_create(
            Artigo(
                titulo_do_periodico=artigo['titulo_do_periodico'],
                titulo_do_artigo=artigo['titulo_do_artigo'],
                volume=artigo['volume'],
                numero=artigo['numero'],
                ano_de_publicacao=artigo['ano_de_publicacao'],
                # autores=autor
            )
            for artigo in artigos
        )
    return render(request, template_name)


def dados_artigos(request):
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', DEFAULT_PAGE_SIZE)

    queryset = Artigo.objects.all()
    if q := request.GET.get('q'):
        queryset = queryset.filter(name__icontains=q)

    paginator = Paginator(queryset, per_page=page_size)
    page = paginator.get_page(page_number)

    return JsonResponse(page2dict(page))

# @loginequired

@csrf_exempt
def dados_xml(request):
    username = request.POST.get('usuario')
    password = request.POST.get('senha')
    user = authenticate(request, username=username, password=password)
    if user is None:
        response_data = {'error': "Senha e/ou usuário inválidos"}
        return JsonResponse(response_data, status=HTTPStatus.UNAUTHORIZED)
    else:
        name_file = request.GET.get('file_xml')
        flag = any(
            filename.name == name_file
            for filename in Path().cwd().parent.glob('**/sc*.xml')
        )
        if not flag:
            arquivos = " - ".join([r.name for r in Path().cwd().parent.glob('**/sc*.xml')])
            response_data = {
                'error': "Arquivo inexistente",
                'files': arquivos
            }
        else:
            response_data = {
                'error': "Tudo OK!",
                'files': name_file
            }
            # path = Path().cwd().parent.glob('**/sc*.xml')
            for filename in Path().cwd().parent.glob('**/sc*.xml'):
                if filename.name == name_file:
                    with open(filename, encoding='utf-8') as fp:
                        tree = ET.parse(fp)
                    artigos = get_artigos_from_xml(tree)
                    # autores = [autor['nome'] for autor in get_autores_from_xml(tree)]
                    # autores = Autor.objects.bulk_create(
                    #     Autor(nome=autor)
                    #     for autor in artigos[0]['autores']
                    # )
                    # Figura.objects.bulk_create(
                    #     Figura(
                    #         rotulo=figura['rotulo'],
                    #         legenda=figura['legenda'],
                    #         imagem=figura['imagem']
                    #     )
                    #     for figura in artigos[0]['figuras']
                    # )

                    artigos = Artigo.objects.bulk_create(
                        Artigo(**artigo) for artigo in artigos
                    )
                    lista_dos_autores = get_autores_from_xml(tree)
                    for autor in lista_dos_autores:
                        autor.artigos.add(*artigos)

                    # artigos = Artigo.objects.bulk_create(
                    #     Artigo(
                    #         titulo_do_periodico=artigo['titulo_do_periodico'],
                    #         titulo_do_artigo=artigo['titulo_do_artigo'],
                    #         volume=artigo['volume'],
                    #         numero=artigo['numero'],
                    #         ano_de_publicacao=artigo['ano_de_publicacao']
                    #     )
                    #     for artigo in artigos
                    # )
                    # autores.artigos.add(*artigos)
                    # artigos.autores.add(*artigos)
                    break

        return JsonResponse(response_data, status=HTTPStatus.OK)

def page2dict(page):
    return {
        'data': [a.to_dict() for a in page],
        'count': page.paginator.count,
        'current_page': page.number,
        'num_pages': page.paginator.num_pages
    }