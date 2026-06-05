from django.shortcuts import render
from .models import DestinoTuristico

# Create your views here.
def index(request):
    destinos = DestinoTuristico.objects.all()
    return render(request, 'index.html', {'destinosHtml' : destinos})
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def destinations(request):
    destinos = DestinoTuristico.objects.all()
    return render(request, 'destinations.html', {'destinosHtml' : destinos})
def news(request):
    return render(request, 'news.html')