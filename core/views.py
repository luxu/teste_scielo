from django.shortcuts import render

from .models import Figura


def index(request):
    template_name = 'core/index.html'
    figuras = Figura.objects.all()
    context = {
        'figuras': figuras
    }
    return render(request, template_name, context)

