"""sistema_fisioterapia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('manage/', admin.site.urls),
    path('',include('core.urls')),
    path('',include('agenda.urls')),
    path('',include('pacientes.urls')),
    path('',include('controle_usuarios.urls')),
    path('',include('atendimento.urls')),
    path('',include('financeiro.urls')),
    path('',include('website.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = urlpatterns + [
        path('__debug__/', include(debug_toolbar.urls)),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#confid admin labels
admin.site.site_header = 'PISCICOCENTER ADMIN'
admin.site.site_title  = 'Piscicocenter Portal'
admin.site.index_title  = 'BEM VINDO AO PISCICOCENTER ADMIN'