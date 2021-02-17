from django.urls import path
from django.conf import settings
from PDF import viewsPDF

urlpatterns = [
     path('reporte_personas_pdf/<int:user_id>',viewsPDF.PDFReparaciones.as_view(), name="pdf"),

]