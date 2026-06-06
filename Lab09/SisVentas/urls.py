from django.urls import path
from .views import DetalleDeVentaPdf
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('venta/<int:sale_id>/pdf/', DetalleDeVentaPdf.as_view(), name='venta_pdf'),
    path('send/venta/<int:sale_id>/', views.send, name='enviar_correo')
]
