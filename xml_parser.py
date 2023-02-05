import xml.etree.ElementTree as ET
from pathlib import Path


def save_info_image(fig, figures):
    label = fig.find('.//label').text
    title = ''.join(fig.find('.//caption/title').itertext())
    for g in fig.findall('.//alternatives/graphic'):
        for k in g.attrib:
            if 'href' in k:
                url_image = g.attrib[k]
                item = {
                    'id': fig.attrib['id'],
                    'rotulo': label,
                    'legenda': title,
                    'imagem': url_image
                }
                figures.append(item)
    return figures


def get_figuras_from_xml(tree):
    figures = []
    if xml_figures := tree.findall('.//sec/fig-group'):
        for fig in xml_figures:
            for f in fig.findall('fig'):
                for lang in f.attrib.values():
                    if lang == 'en':
                        save_info_image(fig, figures)
    else:
        xml_figures = tree.findall('.//sec/fig')
        for fig in xml_figures:
            save_info_image(fig, figures)
    return figures


def get_autores_from_xml(tree):
    authors = []
    for autor in tree.findall('.//front//article-meta//contrib-group//contrib//name'):
        sobrenome = autor.find('surname').text
        nome = autor.find('given-names').text
        items = {'nome': " ".join((nome, sobrenome))}
        authors.append(items)
    return authors


def get_artigos_from_xml(tree):
    artigos = []
    numero = 0
    lista_dos_autores = get_autores_from_xml(tree)
    lista_das_figuras = get_figuras_from_xml(tree)
    autores = [autores['nome'] for autores in lista_dos_autores]
    figuras = list(lista_das_figuras)
    for artigo in tree.findall('.//front'):
        titulo_do_periodico = artigo.find('.//journal-title').text
        titulo_do_artigo = artigo.find('.//article-title').text
        try:
            volume = artigo.find('.//x').text
        except AttributeError:
            volume = artigo.find('.//volume').text
        ano_de_publicacao = artigo.find('article-meta//pub-date//year').text
        items = {
            'titulo_do_periodico': titulo_do_periodico,
            'titulo_do_artigo': titulo_do_artigo,
            'volume': volume,
            'numero': numero,
            'ano_de_publicacao': ano_de_publicacao,
            'autores': autores,
            'figuras': figuras
        }
        artigos.append(items)
    return artigos


def main():
    for file_name in Path().glob('**/*.xml'):
        print(f'{"+" * 50}  {file_name}  {"+" * 50}')
        with open(file_name, encoding='utf-8') as fp:
            tree = ET.parse(fp)
            artigos = get_artigos_from_xml(tree)
            for indice, artigo in enumerate(artigos):
                titulo_do_periodico = artigo["titulo_do_periodico"]
                titulo_do_artigo = artigo["titulo_do_artigo"]
                volume = artigo["volume"]
                numero = artigo["numero"]
                ano_de_publicacao = artigo["ano_de_publicacao"]
                autores = artigo["autores"]
                figuras = artigo["figuras"]
                print(f'{titulo_do_periodico}\n{titulo_do_artigo}\nVolume..: {volume}'
                      f'\nNumero..:{numero}\nAno..:{ano_de_publicacao}'
                      f'\nAutores..:{autores}'
                      f'\nFiguras..:{figuras}'
                      f'\n\n{"+" * 50}  {file_name}  {"+" * 50}')


if __name__ == '__main__':
    main()
