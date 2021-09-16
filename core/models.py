from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
  titulo = models.CharField(max_length=100)
  descricao = models.TextField(blank=True, null=True)
  data_evento = models.DateTimeField(verbose_name='Data do evento')
  data_criacao = models.DateTimeField(auto_now=True, verbose_name='Criado em')
  usuario = models.ForeignKey(User, on_delete=models.CASCADE)
  local = models.CharField(max_length=30, blank=True, null=True)
  
  class Meta:
    db_table = 'evento'
    
  def get_data(self):
    return self.data_evento.strftime('%d/%m/%Y %H:%M')
    
  def get_criacao(self):
    return self.data_criacao.strftime('%d/%m/%Y %H:%M:%S')
  
  def get_data_iso(self):
    return self.data_criacao.strftime('%Y-%m-%dT%H:%M')
    
  def get_data_number(self):
    return self.data_evento.strftime('%Y%m%d%H%M')

  def __str__(self):
    return self.titulo