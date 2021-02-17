from django.shortcuts import render
from django.conf import settings
from io import BytesIO
from django.views.generic import View
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import TableStyle, Table, Paragraph
from reportlab.lib.units import cm
from reportlab.lib import colors
from datetime import datetime
from nucleo import models

from django.contrib.auth.decorators import login_required
from nucleo.decorators import client_required, mechanic_required
from django.utils.decorators import method_decorator
 
@method_decorator([login_required,mechanic_required], name='dispatch')
class PDFReparaciones(View):  
     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/logo/default.png'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True) 
        #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 16)
        #Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(230, 790, u"Te Lo Arreglo")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(260, 770, u"Repairs")  

       
    def get(self, request, *args, **kwargs):
       #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        y = 600
        userId = self.kwargs.get('user_id')
        cliente=models.Clientes.objects.get(pk=userId)
        repairs= models.reparaciones.objects.filter(client=cliente, fixed=True)
        self.tabla(pdf, y,repairs)
        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    def tabla(self,pdf,y, reparaciones):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Mechanic','Application date', 'Fixed date', 'Reason','Car', 'observations')
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [(Paragraph(reparacion.mechanic.name+' ' +reparacion.mechanic.lastName ),datetime.strftime(reparacion.dateR,'%dd/%mm/%Y'), datetime.strftime(reparacion.dateA,'%dd/%mm/%Y'), Paragraph(reparacion.reason), Paragraph  (reparacion.car.brand),Paragraph(reparacion.observations)) for reparacion in reparaciones]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[2 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black), 
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla 
        detalle_orden.wrapOn(pdf, 800, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 60,y)             
      