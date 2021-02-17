from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import fields
from nucleo.models import Clientes, UserNucleo
from django.db import transaction

class UserCreationFormClient(UserCreationForm):
    email= forms.EmailField(required=True, help_text="Required, maximum 100 characters")
    DNI=forms.CharField(required = True, help_text="Required, maximum 50 characters")
    name=forms.CharField( required = True, help_text="Required, maximum 50 characters")
    lastName=forms.CharField( required = True, help_text="Required, maximum 100 characters")
    address=forms.CharField( required = True, help_text="Required, maximum 75 characters")
    tel=forms.CharField( required = True, help_text="Required, maximum 30 characters")
    date=forms.DateField(required = True)

    class Meta:
        model=UserNucleo
        fields=('username','password1','password2','email', 'DNI', 'name', 'lastName', 'address', 'tel', 'date')
    
    def email(self):
        value=self.cleaned_data['email']
        if UserNucleo.objects.filter(email=value).exists():
            raise forms.ValidationError("This email is already used, try agan with another email")
        return value

    def save(self, commit=True):
        user=super().save(commit=False)
        user.is_client = True
        user.us_active = False
        user.save()
        dni=self.cleaned_data['DNI']
        name=self.cleaned_data['name']
        lastname=self.cleaned_data['lastName']
        address=self.cleaned_data['address']
        tel=self.cleaned_data['tel']
        date=self.cleaned_data['date']
        client = Clientes.objects.create(user=user, DNI=dni, name=name, lastName=lastname, address=address, tel=tel, date=date)
        return user

class UserAdminForm(UserCreationForm):
    class Meta:
        model=UserNucleo
        fields=('username','password1','password2','is_client','is_mechanic','is_active','is_staff','is_superuser')