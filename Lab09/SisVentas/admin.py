from django.contrib import admin

from .models import User, Client, Product, Sale, Sale_detail

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(Sale_detail)
