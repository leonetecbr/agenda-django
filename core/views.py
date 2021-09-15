from django.shortcuts import render#, redirect
from django.http import HttpResponse
from core.models import Evento
from datetime import date

def get_evento(request, titulo_evento):
  try:
    evento = Evento.objects.get(titulo=titulo_evento)
    response = f'<h1>Evento encontrado!</h1><ul><li>Título: {evento.titulo}</li><li>Descrição: {evento.descricao}</li><li>Data do evento: {evento.data_evento.strftime("%d/%m/%Y %H:%M")}</li><li>Local: {evento.local}</li><li>Criado em: {evento.data_criacao.strftime("%d/%m/%Y %H:%M:%S")}</li><li>Criado por: {evento.usuario}</li></ul>'
  except:
    response = '<h1>Nenhum evento encontrado!</h1>'
  return HttpResponse(response)

def lista_eventos(request):
  usuario = request.user
  eventos = Evento.objects.filter(usuario=usuario)
  data = {'eventos':eventos}
  return render(request, 'agenda.html', data)

#def index(request):
#  return redirect('/agenda')