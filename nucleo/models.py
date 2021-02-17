from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework import serializers
import os


class UserNucleo(AbstractUser):
    is_client = models.BooleanField('Estado de cliente', default=False)
    is_mechanic = models.BooleanField('Estado de mecanico', default=False)
    is_active = models.BooleanField('Activo', default=False)


    class Meta:
        verbose_name=("Usuario")
        verbose_name_plural=("Usuarios")
    


# Create your models here.
class Clientes(models.Model):
    user=models.OneToOneField(UserNucleo, on_delete=models.CASCADE, primary_key=True, default=False, related_name="cliente")
    DNI=models.CharField( max_length=50,verbose_name="DNI")
    name=models.CharField( max_length=50,verbose_name="Nombre")
    lastName=models.CharField( max_length=100,verbose_name="Apellidos")
    address=models.CharField( max_length=75,verbose_name="Direccion")
    tel=models.CharField( max_length=30,verbose_name="Telefono")
    date=models.DateField(verbose_name="FechaNacimiento")

    class Meta:
        verbose_name=("Cliente")
        verbose_name_plural=("Clientes")

    def __str__(self):
        return self.DNI+" "+self.name+" "+self.tel




class coches (models.Model):
    brand=models.CharField( max_length=50,verbose_name="Marca")
    model=models.CharField( max_length=50,verbose_name="Modelo")
    colour=models.CharField( max_length=50,verbose_name="Color")
    dateM=models.DateField(verbose_name="Fecha de Matriculacion")
    image=models.ImageField(upload_to='photos/%Y/%m/%d')
    owner=models.ForeignKey(Clientes, verbose_name=("Cliente"), on_delete=models.CASCADE,related_name='cars')

    class Meta:
        verbose_name = ("Coche ")
        verbose_name_plural = ("Coches")

    def __str__(self):
        return self.brand+" "+self.model

class mecanicos(models.Model):
    
    user=models.OneToOneField(UserNucleo, on_delete=models.CASCADE, primary_key=True, default=False, related_name="mecanico")
    DNI=models.CharField( max_length=50,verbose_name="DNI")
    name=models.CharField( max_length=50,verbose_name="Nombre")
    lastName=models.CharField( max_length=100,verbose_name="Apellidos")
    direction=models.CharField( max_length=75,verbose_name="Direccion")
    tel=models.CharField( max_length=30,verbose_name="Telefono")
    date=models.DateField(verbose_name="FechaNacimiento")

    class Meta:
        verbose_name = ("Mecanico")
        verbose_name_plural = ("Mecanicos")

    def __str__(self):
        return self.DNI+" "+self.name+" "+self.tel

class noticias(models.Model):
    
    title=models.CharField(verbose_name="Titulo", max_length=100)
    text=models.CharField(verbose_name="Texto", max_length=200)
    photo=models.ImageField(verbose_name="Foto", upload_to='News/%Y/%m/%d')
    dateC=models.DateField(verbose_name="FechaCreacion", auto_now_add=True)
    dateU=models.DateField(verbose_name="FechaModificacion", auto_now=True)
    mechanic=models.ForeignKey(mecanicos, verbose_name=("Mecanico"), on_delete=models.CASCADE,related_name='news')
    class Meta:
        verbose_name = ("Noticia")
        verbose_name_plural = ("Noticias")

    def __str__(self):
        return self.title+" "+self.text


class reparaciones(models.Model):
    dateR=models.DateTimeField(verbose_name="FechaSolicitud",auto_now_add=True)
    dateA=models.DateTimeField(verbose_name="FechaArreglo",auto_now=True, null=True)
    reason=models.CharField( max_length=300,verbose_name="Motivo")
    observations=models.CharField( max_length=500,verbose_name="Observaciones")
    fixed=models.BooleanField(verbose_name="Arreglado",null=True)
    client=models.ForeignKey(Clientes, verbose_name=("Cliente"), on_delete=models.CASCADE,related_name='repairs')
    car=models.ForeignKey(coches, verbose_name=("Coche"), on_delete=models.CASCADE, related_name='repairs')
    mechanic=models.ForeignKey(mecanicos, verbose_name=("Mecanico"), on_delete=models.CASCADE,related_name='repairs', null=True)


    class Meta:
        verbose_name=("Reparacion")
        verbose_name_plural=("Reparaciones")

    def __str__(self):
        return self.reason+" "+self.observations


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model= Clientes
        fields=['user','DNI','name','lastName','address','tel','date']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserNucleo
        fields=['is_client']