import xml.etree.ElementTree as ET
from http import HTTPStatus
from pathlib import Path

from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
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


def dados_artigos(request):
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', DEFAULT_PAGE_SIZE)

    queryset = Artigo.objects.all()
    if q := request.GET.get('q'):
        queryset = queryset.filter(name__icontains=q)

    paginator = Paginator(queryset, per_page=page_size)
    page = paginator.get_page(page_number)

    return JsonResponse(page2dict(page))


@csrf_exempt
def dados_xml(request):
    username = request.POST.get('usuario')
    password = request.POST.get('senha')
    user = authenticate(request, username=username, password=password)
    if user is None:
        response_data = {'error': "Usuário e/ou senha  inválidos"}
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
                'file': arquivos
            }
        else:
            response_data = {
                'success': "Tudo OK!",
                'file': name_file
            }
            for filename in Path().cwd().parent.glob('**/sc*.xml'):
                if filename.name == name_file:
                    with open(filename, encoding='utf-8') as fp:
                        tree = ET.parse(fp)
                    autores_do_xml = list(get_autores_from_xml(tree))
                    autores = Autor.objects.bulk_create(
                        Autor(**autor) for autor in autores_do_xml
                    )
                    artigos_do_xml = list(get_artigos_from_xml(tree))
                    artigos = Artigo.objects.bulk_create(
                        Artigo(
                            titulo_do_periodico=artigo['titulo_do_periodico'],
                            titulo_do_artigo=artigo['titulo_do_artigo'],
                            volume=artigo['volume'],
                            numero=artigo['numero'],
                            ano_de_publicacao=artigo['ano_de_publicacao']
                        )
                        for artigo in artigos_do_xml
                    )
                    for autor in autores:
                        autor.artigos.add(*artigos)
                    figuras = get_figuras_from_xml(tree)
                    Figura.objects.bulk_create(
                        Figura(
                            rotulo=figura['rotulo'],
                            legenda=figura['legenda'],
                            imagem=figura['imagem']
                        )
                        for figura in figuras
                    )
        return JsonResponse(response_data, status=HTTPStatus.OK)


def page2dict(page):
    return {
        'data': [a.to_dict() for a in page],
        'count': page.paginator.count,
        'current_page': page.number,
        'num_pages': page.paginator.num_pages
    }
