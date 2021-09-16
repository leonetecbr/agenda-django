from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from core.models import Evento
from django.http.response import *
from datetime import datetime

@login_required(login_url='/login/')
def get_evento(request, id):
  data_atual = datetime.now().strftime('%Y%m%d%H%M')
  usuario = request.user
  try:
    evento = Evento.objects.get(id=id, usuario=usuario)
  except:
    raise Http404()
  data = {'evento':evento, 'data_atual':data_atual}
  return render(request, 'agenda_id.html', data)

@login_required(login_url='/login/')
def lista_eventos(request):
  data_atual = datetime.now().strftime('%Y%m%d%H%M')
  usuario = request.user
  eventos = Evento.objects.filter(usuario=usuario)
  data = {'eventos':eventos, 'data_atual':data_atual}
  return render(request, 'agenda.html', data)

@login_required(login_url='/login/')
def json_eventos(request):
  usuario = request.user
  eventos = list(Evento.objects.filter(usuario=usuario).values('id', 'titulo', 'descricao', 'local', 'data_evento', 'data_criacao'))
  if len(eventos) > 0:
    data = {'code':200, 'eventos':eventos}
  else:
    data = {'code':404, 'message':'Nenhum evento encontrado!'}
    
  return JsonResponse(data, safe=False)


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
      messages.error(request, 'Usuário ou senha inválidos!')
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
    if (Evento.objects.create(titulo=titulo,
                          data_evento=date,
                          descricao=desc,
                          usuario=usuario,
                          local=local)):
      return redirect('/agenda/')
    data = {'desc':desc, 'titulo':titulo, 'date':date, 'local':local}
  else:
    data = None
  return render(request, 'agenda_new.html', data)

@login_required(login_url='/login/')
def exclui_evento(request, id):
  usuario = request.user
  try:
    evento = Evento.objects.get(id=id)
  except:
    messages.error(request, 'Evento solicitado não encontrado!')
  else:
    if usuario == evento.usuario:
      evento.delete()
    else:
      messages.error(request, 'Você não tem permissão para excluir o evento solicitado!')
  return redirect('/agenda/')

@login_required(login_url='/login/')
def edita_evento(request, id):
  usuario = request.user
  try: 
    evento = Evento.objects.get(id=id)
  except:
    messages.error(request, 'Evento solicitado não encontrado!')
  else:
    if usuario == evento.usuario:
      if request.POST:
        titulo = request.POST.get('title')
        date = request.POST.get('data')
        desc = request.POST.get('desc')
        local = request.POST.get('local')
        try:
          evento.titulo = titulo
          evento.data_evento=date
          evento.descricao=desc
          evento.local=local
          evento.save()
          return redirect('/agenda/'+str(id))
        except:
          data = {'desc':desc, 'titulo':titulo, 'date':date, 'local':local, 'evento':evento}
      else:
        data = {'evento':evento}
      return render(request, 'agenda_edit.html', data)
    else:
      messages.error(request, 'Você não tem permissão para editar o evento solicitado!')
  return redirect('/agenda/')