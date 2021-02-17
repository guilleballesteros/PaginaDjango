from django import forms
from django.forms import widgets
from nucleo import models
from datetime import datetime


class CreateCarForm(forms.ModelForm):
    class Meta:
        model=models.coches
        fields=('brand','model','colour','dateM', 'image')
        
        widgets={
            'brand':forms.TextInput(attrs={'class':'form-control mb-4', 'placeholder':'Insert the DNI'}),
            'model':forms.TextInput(attrs={'class':'form-control mb-4', 'placeholder':'Insert the address'}),
            'colour':forms.TextInput(attrs={'class':'form-control mb-4', 'placeholder':'Insert the telephone number'}),
            'dateM': forms.DateInput(attrs={'type':'text'}),

        }

class CreatenewsForm(forms.ModelForm):
    class Meta:
        model=models.noticias
        fields=('title','text','photo')
        
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control mb-4', 'placeholder':'Insert the title'}),
            'text':forms.Textarea(attrs={'class':'form-control mb-4', 'placeholder':'Insert the text'}),
        }
    

class CreateReparacionForm(forms.ModelForm):
    class Meta:
        model=models.reparaciones
        fields=('reason',)

        widgets={
            'reason':forms.Textarea(attrs={'class':'form-control mb-4', 'placeholder':'Insert the reason'})
        }


class UpdateReparacionForm(forms.ModelForm):
    class Meta:
        model=models.reparaciones
        fields=('observations',)

        widgets={
            'observations':forms.Textarea(attrs={'class':'form-control mb-4', 'placeholder':'Insert the reason'})
        }