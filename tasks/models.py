from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  created = models.DateTimeField(auto_now_add=True)
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title + ' - by ' + self.user.username

  
class Prediction(models.Model):
  nombres = models.CharField(max_length=150)
  apellidos = models.CharField(max_length=150)
  numero_documento = models.CharField(max_length=15)
  numero_embarazos = models.IntegerField()
  glucuosa = models.DecimalField(max_digits=15,decimal_places=3)
  presion_arterial = models.DecimalField(max_digits=15,decimal_places=3)
  espesor_piel = models.DecimalField(max_digits=15,decimal_places=3)
  insulina = models.DecimalField(max_digits=15,decimal_places=3)
  indice_masa_corporal = models.DecimalField(max_digits=15,decimal_places=3)
  funcion_pedigree_diabetes = models.DecimalField(max_digits=15,decimal_places=3)
  edad = models.IntegerField()
  resultado = models.DecimalField(max_digits=15,decimal_places=3,null=True, blank=True)
  created = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.nombres +' '+ self.apellidos + ' - ' + self.user.username

