from django.db import models

# Create your models here.
class DestinoTuristico(models.Model):
    nombre_ciudad = models.CharField(max_length=50)
    descripcion_ciudad = models.TextField()
    imagen_ciudad = models.ImageField(upload_to='fotos_destinos/')
    precioTour = models.DecimalField(max_digits=8, decimal_places=2)
    ofertaTour = models.BooleanField()
    def __str__(self):
        return self.nombre_ciudad