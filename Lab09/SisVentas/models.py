from django.db import models
from django.db.models import Sum

class User(models.Model):
    user_name = models.CharField(max_length=20)
    def __str__(self):
        return self.user_name
    
class Client(models.Model):
    client_name = models.CharField(max_length=20)
    whoulesaler = models.BooleanField()
    def __str__(self):
        return self.client_name
    
class Product(models.Model):

    product_name = models.CharField(max_length=20)
    product_description = models.CharField(max_length=100)
    price_buy = models.DecimalField(max_digits=6, decimal_places=2)
    price_sale = models.DecimalField(max_digits=6, decimal_places=2)
    price_whoulesale = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.product_name
    
class Sale(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    products = models.ManyToManyField(Product, through='Sale_detail')

    def update_total(self):
        total = self.sale_detail_set.aggregate(total_suma = Sum('subtotal'))['total_suma']
        self.total = total or 0.00
        self.save()
    def __str__(self):
        date = self.date.strftime("%Y-%m-%d - %H:%M")
        return f"Venta {self.id} - Total: {self.total} | ({date})"
    
class Sale_detail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()
    price_unit = models.DecimalField(max_digits=6, decimal_places=2, editable=False)
    subtotal = models.DecimalField(max_digits=7, decimal_places=2, editable=False)

    def save(self,*args, **kwargs):
        if self.sale.client.whoulesaler:
            self.price_unit = self.product.price_whoulesale
        else:
            self.price_unit = self.product.price_sale
        self.subtotal = self.price_unit * self.amount
        super().save(*args, **kwargs)
        self.sale.update_total()
    def delete(self, *args, **kwargs):
        sale = self.sale
        super().delete(*args, **kwargs)
        sale.update_total()
    def __str__(self):
        return f"Venta {self.sale.id} - {self.amount} unidades de {self.product.product_name} | {self.subtotal}"