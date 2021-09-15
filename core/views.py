from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from core.models import Evento
from datetime import date

@login_required(login_url='/login/')
def get_evento(request, titulo_evento):
  try:
    evento = Evento.objects.get(titulo=titulo_evento, usuario=usuario)
    response = f'<h1>Evento encontrado!</h1><ul><li>Título: {evento.titulo}</li><li>Descrição: {evento.descricao}</li><li>Data do evento: {evento.data_evento.strftime("%d/%m/%Y %H:%M")}</li><li>Local: {evento.local}</li><li>Criado em: {evento.data_criacao.strftime("%d/%m/%Y %H:%M:%S")}</li><li>Criado por: {evento.usuario}</li></ul>'
  except:
    response = '<h1>Nenhum evento encontrado!</h1>'
  return HttpResponse(response)

@login_required(login_url='/login/')
def lista_eventos(request):
  usuario = request.user
  eventos = Evento.objects.filter(usuario=usuario)
  data = {'eventos':eventos}
  return render(request, 'agenda.html', data)

def login_user(request):
  if request.user.is_authenticated:
    return redirect('/agenda/')
  if request.POST:
    username = request.POST.get('username')
    password = request.POST.get('password')
    usuario = authenticate(username=username, password=password)
    if not usuario is None:
      login(request, usuario)
      to = '/agenda/' if request.GET.get('next') is None else request.GET.get('next')
      return redirect(to)
    else:
      messages.error(request, "Usuário ou senha inválidos!")
  data = {'username':username} if request.POST else None
  return render(request, 'login.html', data)

@login_required(login_url='/login/')
def logout_user(request):
  logout(request)
  return redirect('/login/')

#def index(request):
#  return redirect('/agenda')

@login_required(login_url='/login/')
def novo_evento(request):
  if request.POST:
    usuario = request.user
    titulo = request.POST.get('title')
    date = request.POST.get('data')
    desc = request.POST.get('desc')
    local = request.POST.get('local')
    data = {'desc':desc, 'titulo':titulo, 'date':date, 'local':local}
    Evento.objects.create(titulo=titulo,
                          data_evento=date,
                          descricao=desc,
                          usuario=usuario)
    return redirect('/agenda/')
  else:
    data = None
  return render(request, 'agenda_new.html', data)