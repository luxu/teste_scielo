from django.contrib import admin

from .models import Artigo, Figura, Autor

admin.site.register([Artigo, Figura, Autor])
