from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Crackers(models.Model):
    image = models.ImageField(upload_to='crackimages/')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class carosel(models.Model):
    slideimage = models.ImageField(upload_to='slideimage/')

class similarCrackers(models.Model):
    name = models.ForeignKey(Crackers, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='similarimage/')
    similarname = models.CharField(max_length=100)
    actual_price = models.TextField(null=True)
    discount_price = models.TextField()
    content = models.TextField(default="new")


    def __str__(self):
        return f"{self.name} - {self.similarname}"


class CartItem(models.Model):
    username = models.TextField()
    image = models.ImageField(upload_to='cart/')
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_discount = models.DecimalField(max_digits=5, decimal_places=2)

    def calculate_total(self):
        discounted_price = self.product_price * (1 - self.product_discount / 100)
        return discounted_price * self.quantity

    def __str__(self):
        return self.product_name


class Address(models.Model):
    User = models.TextField()
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)

    def __str__(self):
        return self.name   

class Orders(models.Model):
    username = models.TextField()
    quantitity=models.IntegerField(default=1)
    image = models.ImageField(upload_to='cart/')
    product_id = models.IntegerField(default=0)
    product_name = models.CharField(max_length=255, default='')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    product_discount = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))

    def calculate_total(self):
        discounted_price = self.product_price * (1 - self.product_discount / 100)
        return discounted_price * self.quantity

    def __str__(self):
        return self.product_name

