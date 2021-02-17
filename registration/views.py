from django.shortcuts import render
from django import forms
from django.views.generic import CreateView
from django.urls import reverse_lazy

from registration.forms import UserCreationFormClient

# Create your views here.

class SignUpView(CreateView):
    form_class=UserCreationFormClient
    template_name='registration/signin.html'

    def get_success_url(self):
        return reverse_lazy('login')+'?SignIn'
    
    def get_form(self,form_class=None):
        form=super(SignUpView, self).get_form()
        form.fields['username'].widget=forms.TextInput(attrs={'class':'form-control mb-4', 'placeholder':'Insert the username'})
        form.fields['email'].widget=forms.TextInput(attrs={'class':'form-control mb-4', 'placeholder':'Insert the email'})
        form.fields['name'].widget=forms.TextInput(attrs={'class':'form-control mb-4', 'placeholder':'Insert the name'})
        form.fields['lastName'].widget=forms.TextInput(attrs={'class':'form-control mb-4', 'placeholder':'Insert the lastname'})
        form.fields['DNI'].widget=forms.TextInput(attrs={'class':'form-control mb-4', 'placeholder':'Insert the DNI'})
        form.fields['address'].widget=forms.TextInput(attrs={'class':'form-control mb-4', 'placeholder':'Insert the address'})
        form.fields['tel'].widget=forms.TextInput(attrs={'class':'form-control mb-4', 'placeholder':'Insert the telephone number'})
        form.fields['date'].widget=forms.DateInput(attrs={'class':'form-control mb-4', 'placeholder':'Insert the birth date','type':'date'})
        form.fields['password1'].widget=forms.PasswordInput(attrs={'class':'form-control mb-4', 'placeholder':'Insert the password'})
        form.fields['password2'].widget=forms.PasswordInput(attrs={'class':'form-control mb-4', 'placeholder':'Insert the password2'})
        return form
