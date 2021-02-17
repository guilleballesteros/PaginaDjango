from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from registration import views

urlpatterns = [
    path('SignIn',views.SignUpView.as_view(), name="SignIn"),
    
]