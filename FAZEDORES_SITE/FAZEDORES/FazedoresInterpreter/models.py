from django.db import models
from django.utils import timezone

class Algoritmo(models.Model):
    author = models.ForeignKey('auth.User')
    algoritmo = models.TextField()

    def enviar(self):
        self.save()

    def __str__(self):
        return self.author
