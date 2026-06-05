from django.shortcuts import render
from django.core.mail import send_mail

def send(request):
    send_mail(
        'Hi',
        'Hi desde Django',
        'jcusiq@unsa.edu.pe',
        ['comogeb679@brixozu.com'],
        fail_silently=False
        )
    return render(request, 'send/send.html')

