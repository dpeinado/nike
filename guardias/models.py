from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from nike.users.models import User
# Create your models here.

@python_2_unicode_compatible
class Organizacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Centro(models.Model):
    nombre = models.CharField(max_length=100)
    organizacion = models.ForeignKey(Organizacion, blank=True, null=True)
    supervisor = models.ForeignKey(User, blank=True, null=True)