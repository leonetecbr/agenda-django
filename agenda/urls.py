"""agenda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from core import views
from django.views.generic import RedirectView

urlpatterns = [
    #path('', views.index),
    path('', RedirectView.as_view(url='/agenda/')),
    path('admin/', admin.site.urls),
    path('login/', views.login_user),
    path('logout/', views.logout_user),
    path('agenda/<int:id>/', views.get_evento),
    path('agenda/delete/<int:id>/', views.exclui_evento),
    path('agenda/edit/<int:id>/', views.edita_evento),
    path('agenda/', views.lista_eventos),
    path('agenda/json/', views.json_eventos),
    path('agenda/new/', views.novo_evento),
]
