from reportlab.pdfgen import canvas
from reportlab.platypus import TableStyle, Table, Paragraph
from reportlab.lib.units import cm
from reportlab.lib import colors
from datetime import datetime
from django.forms.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django import forms
from nucleo import models,forms
from django.http import HttpResponse, response
from django.utils.datastructures import MultiValueDictKeyError
import os
from django.conf import settings
from io import BytesIO
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from nucleo.decorators import client_required, mechanic_required
from django.utils.decorators import method_decorator
        
# Vista inicial


def index(request):
    noticias=models.noticias.objects.all()[0:5]
    data={
        'title':'News',
        'icon': 'far fa-newspaper',
        'noticias': noticias
    }
    return render(request,'nucleo/pruebas.html',data)

# Vistas de coches

@method_decorator([login_required,client_required], name='dispatch')
class carListView(ListView):
    model=models.coches
    template_name='nucleo/Coches/index.html'

    def get_queryset(self):
        return self.request.user.cliente.cars.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'List of your cars'
        context["icon"] = 'fas fa-search'
        return context
    
@method_decorator([login_required,client_required], name='dispatch')
class CarCreateView(CreateView):
    model=models.coches
    template_name='nucleo/Coches/create.html'
    form_class=forms.CreateCarForm
    success_url="/nucleo/listCar/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Create a new Car'
        context["icon"] = 'fas fa-plus'
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner=self.request.user.cliente
        return super(CarCreateView,self).form_valid(form)

@method_decorator([login_required,client_required], name='dispatch')
class CarUpdateView(UpdateView):
    model=models.coches
    template_name='nucleo/Coches/create.html'
    form_class=forms.CreateCarForm
    success_url="/nucleo/listCar/"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update the Car'
        context["icon"] = 'fas fa-edit'
        return context

    def form_valid(self, form):
        coche=models.coches.objects.get(pk=self.get_object().id)
        imagen=form.cleaned_data['image']
        if("/media/"+str(imagen) != coche.image.url):
            coche.image.delete()
        return super().form_valid(form)
    
    
@method_decorator([login_required,client_required], name='dispatch')  
class CarDeleteView(DeleteView):
    model=models.coches
    template_name='nucleo/Coches/delete.html'
    success_url="/nucleo/listCar/"  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Delete the Car'
        context["icon"] = 'fas fa-trash'
        return context  
    def delete(self, request, *args, **kwargs):
        self.get_object().image.delete()
        return super().delete(request, *args, **kwargs) 
            
# Vistas de Reparaciones
@method_decorator([login_required,client_required], name='dispatch')
class CarRepairView(CreateView):
    model=models.reparaciones
    template_name='nucleo/reparaciones/form.html'
    form_class=forms.CreateReparacionForm
    success_url="/nucleo/listCar/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Apply for a repair'
        context["icon"] = 'fas fa-tools'
        return context

    def form_valid(self, form):
        coche_id = self.kwargs.get('coche_id')
        coche=models.coches.objects.get(pk=coche_id)
        self.object = form.save(commit=False)
        self.object.fixed=False
        self.object.car=coche
        self.object.client=self.request.user.cliente
        return super(CarRepairView,self).form_valid(form)
@method_decorator([login_required,client_required], name='dispatch')
class ListReparacionesCliente(ListView):
    model=models.reparaciones
    template_name='nucleo/reparaciones/repairsDone.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reparaciones"] = models.reparaciones.objects.filter(client=self.request.user.cliente, fixed=True)
        return context
@method_decorator([login_required,mechanic_required], name='dispatch')
class CarListReparaciones(ListView):
    model=models.coches
    template_name='nucleo/reparaciones/repairsDone.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'List of repairs'
        context["icon"] = 'fas fa-search'
        coche=models.coches.objects.get(pk=self.kwargs.get('coche_id'))
        context["reparaciones"] = models.reparaciones.objects.filter(car=coche, fixed=True)
        return context
@method_decorator([login_required,mechanic_required], name='dispatch')
class updateRepair(UpdateView):
    model=models.reparaciones
    template_name='nucleo/reparaciones/repair.html'
    form_class=forms.UpdateReparacionForm
    success_url="/nucleo/listRepairs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Repairing the car'
        context["icon"] = 'fas fa-tools'
        return context
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.mechanic=self.request.user.mecanico
        self.object.fixed=True
        return super(updateRepair,self).form_valid(form)

@method_decorator([login_required,mechanic_required], name='dispatch')
class repairsListView(ListView):
    model=models.reparaciones
    template_name='nucleo/reparaciones/index.html'

    def get_queryset(self):
        return models.reparaciones.objects.filter(fixed=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'List of undone repairs'
        context["icon"] = 'fas fa-search'
        return context  

# Vistas de clientes
@method_decorator([login_required,mechanic_required], name='dispatch')
class clientesListView(ListView):
    model=models.Clientes
    template_name='nucleo/Clientes/index.html'
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='List of the clients'
        context['icon']='fas fa-search'
        return context


@method_decorator([login_required,mechanic_required], name='dispatch')
class CarListClient(ListView):
    model=models.coches
    template_name='nucleo/Coches/index.html'
    def get_context_data(self, **kwargs):
            context= super().get_context_data(**kwargs)
            context['title']='List of the News'
            context['icon']='fas fa-search'
            return context
    def get_queryset(self):
        cliente=models.Clientes.objects.get(pk= self.kwargs.get('pk'))
        return models.coches.objects.filter(owner=cliente)
    

# Vistas de noticias
@method_decorator([login_required,mechanic_required], name='dispatch')
class newsListView(ListView):
    model=models.noticias
    template_name='nucleo/Noticias/index.html'
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='List of the News'
        context['icon']='fas fa-search'
        return context

    def get_queryset(self):
        return self.request.user.mecanico.news.all()
@method_decorator([login_required,mechanic_required], name='dispatch')   
class NewsCreateView(CreateView):
    model=models.noticias
    template_name='nucleo/Noticias/create.html'
    form_class=forms.CreatenewsForm
    success_url="/nucleo/listNews/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Create a new'
        context["icon"] = 'fas fa-plus'
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.mechanic=self.request.user.mecanico
        return super(NewsCreateView,self).form_valid(form)
@method_decorator([login_required,mechanic_required], name='dispatch')
class NewUpdateView(UpdateView):
    model=models.noticias
    template_name='nucleo/Noticias/create.html'
    form_class=forms.CreatenewsForm
    success_url="/nucleo/listNews/"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update the New'
        context["icon"] = 'fas fa-edit'
        return context
    def form_valid(self, form):
        noticia=models.noticias.objects.get(id=self.get_object().id)
        imagen=form.cleaned_data['photo']
        if("/media/"+str(imagen) != noticia.photo.url):
            noticia.image.delete()
        return super().form_valid(form)
@method_decorator([login_required,mechanic_required], name='dispatch')
class NewDeleteView(DeleteView):
    model=models.noticias
    template_name='nucleo/Noticias/delete.html'
    success_url="/nucleo/listNews/"  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Delete the News'
        context["icon"] = 'fas fa-trash'
        return context   
    def delete(self, request, *args, **kwargs):
        self.get_object().photo.delete()
        return super().delete(request, *args, **kwargs) 


#API

class clientes_APIView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self,request,format=None, *args, **kwargs):
        clientes=models.Clientes.objects.all()
        serializer=models.ClientSerializer(clientes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer=models.ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class clientes_APIVIEWDetail(APIView):
    permission_classes= [IsAuthenticated]
    def get_object(self,pk):
        try:
            return models.Clientes.objects.get(pk=pk)
        except models.Clientes.DoesNotExist:
            raise response.Http404

    def get(self,request,pk,format=None):
        client=self.get_object(pk)
        serializer= models.ClientSerializer(client)
        return Response(serializer.data)

    def put(self,request,pk,format=None):
        client=self.get_object(pk)
        serializer= models.ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None):
        client=self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)

class user_APIView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self,request,format=None, *args, **kwargs):
        users=models.UserNucleo.objects.all()
        serializer=models.UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer=models.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class users_APIVIEWDetail(APIView):
    permission_classes= [IsAuthenticated]
    def get_object(self,pk):
        try:
            return models.UserNucleo.objects.get(pk=pk)
        except models.UserNucleo.DoesNotExist:
            raise response.Http404

    def get(self,request,pk,format=None):
        user=self.get_object(pk)
        serializer= models.UserSerializer(user)
        return Response(serializer.data)

    def put(self,request,pk,format=None):
        user=self.get_object(pk)
        serializer= models.UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None):
        user=self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)


#CORS

class CorsView(APIView):
    def get(self,request,format=None):
        return Response({'detail': 'GET Response'})
    def post(self,request,format=None):
        try:
            data=request.data
        except ParseError as error:
            return Response(
                'invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        if "username" not in data or "password" not in data:
            return Response(
                'Wrong credentials',
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user= models.UserNucleo.objects.get(username=data["username"])
        if user.is_staff==False:
             return Response(
                'The user is not the admin',
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not user:
            return Response(
                'No default user, please create one',
                status=status.HTTP_404_NOT_FOUND
            )
        token=Token.objects.get_or_create(user=user)
        return Response({'detail':'POST answer','Token': token[0].key})