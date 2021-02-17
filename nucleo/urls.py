from django.urls import path
from django.conf import settings
from nucleo import views

urlpatterns = [
    path('listCar/', views.carListView.as_view(), name="listCar"),
    path('ApplyrepairCar/<int:coche_id>', views.CarRepairView.as_view(), name="ArepairCar"),
    path('createCar', views.CarCreateView.as_view(), name="createCar"),
    path('updateCar/<int:pk>', views.CarUpdateView.as_view(), name="updateCar"),
    path('deleteCar/<int:pk>', views.CarDeleteView.as_view(), name="deleteCar"),
    path('listClients/', views.clientesListView.as_view(), name="listClients"),
    path('listCarClient/<int:pk>',views.CarListClient.as_view(),name="carsClient"),
    path('listCarrepairs/<int:coche_id>',views.CarListReparaciones.as_view(),name="carRepairs"),
    path('listRepairs/', views.repairsListView.as_view(), name="listRepairs"),
    path('listRepairsClient/', views.ListReparacionesCliente.as_view(), name="listRepairsC"),
    path('repairCar/<int:pk>', views.updateRepair.as_view(), name="repairCar"),
    path('listNews/', views.newsListView.as_view(), name="listNews"),
    path('createNew/', views.NewsCreateView.as_view(), name="createNew"),
    path('updateNew/<int:pk>', views.NewUpdateView.as_view(), name="updateNew"),
    path('deleteNew/<int:pk>', views.NewDeleteView.as_view(), name="deleteNew"),
    path('api/clients',views.clientes_APIView.as_view()),
    path('api/clients/<int:pk>',views.clientes_APIVIEWDetail.as_view()),
    path('api/login',views.CorsView.as_view()),

]