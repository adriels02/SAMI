from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    data_de_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")
    enviado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Enviado por")
    arquivo = models.FileField(upload_to='documents/', verbose_name="Arquivo")

    def __str__(self):
        return self.titulo
    