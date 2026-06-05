from django.views import View
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa
from django.shortcuts import render

from .models import Sale

def index(request):
    ventas = Sale.objects.all()
    return render(request, 'index.html', {'VentasHtml': ventas})

class DetalleDeVentaPdf(View):
    def get(self, request, sale_id, *args, **kwargs):

        venta = get_object_or_404(Sale, id=sale_id)
        detalles = venta.sale_detail_set.all()
        template = get_template('reportes/factura.html')
        context = {
            'venta': venta,
            'detalles': detalles,
        }

        html_string = template.render(context)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f"inline; filename='Venta {venta.id}.pdf'"

        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('Ocurrió un error al generar el PDF', status=500)
        return response