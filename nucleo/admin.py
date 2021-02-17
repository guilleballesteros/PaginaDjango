from django import forms
from django.contrib import admin
import hashlib
from django.contrib.auth.forms import UserCreationForm
from nucleo.models import UserNucleo, coches,Clientes,mecanicos,reparaciones,noticias
from registration.forms import UserAdminForm

class ClientsAdmin(admin.ModelAdmin):
    model=Clientes
    ordering=['name']
    list_per_page=4
    def clean_name(self):
        if(len(self.cleaned_data['name'])<3):
            raise forms.ValidationError('The name is very short')
        else:
            return self.cleaned_data['name']

    def clean_lastName(self):
        if(len(self.cleaned_data['lastName'])<3):
            raise forms.ValidationError('The lastName is very short')
        else:
            return self.cleaned_data['lastName']
    def clean_lastName(self):
        if(len(self.cleaned_data['lastName'])<3):
            raise forms.ValidationError('The lastName is very short')
        else:
            return self.cleaned_data['lastName']
    

class MechanicsAdmin(admin.ModelAdmin):
    model=mecanicos
    ordering=['name']
    list_per_page=4
    def clean_name(self):
        if(len(self.cleaned_data['name'])<3):
            raise forms.ValidationError('The name is very short')
        else:
            return self.cleaned_data['name']

    def clean_lastName(self):
        if(len(self.cleaned_data['lastName'])<3):
            raise forms.ValidationError('The lastName is very short')
        else:
            return self.cleaned_data['lastName']
    def clean_lastName(self):
        if(len(self.cleaned_data['lastName'])<3):
            raise forms.ValidationError('The lastName is very short')
        else:
            return self.cleaned_data['lastName']


class RepairsAdmin(admin.ModelAdmin):
    model=reparaciones
    ordering=['dateR']
    list_per_page=4

class NewsAdmin(admin.ModelAdmin):
    model=noticias
    ordering=['title']
    list_per_page=4

class CarsAdmin(admin.ModelAdmin):
    model=coches
    ordering=['brand']
    list_per_page=4

class UserAdmin(admin.ModelAdmin):
    model = UserNucleo
    ordering=['username']
    list_per_page=4
    form=UserAdminForm
    def clean_password(self):
        password=self.cleaned_data['password']
        password=hashlib.md5(password)
        return password
# Register your models here.
admin.site.register(Clientes,ClientsAdmin)
admin.site.register(mecanicos,MechanicsAdmin)
admin.site.register(coches,CarsAdmin)
admin.site.register(reparaciones,RepairsAdmin)
admin.site.register(noticias,NewsAdmin)
admin.site.register(UserNucleo,UserAdmin)