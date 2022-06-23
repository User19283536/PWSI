from django.db import models
import datetime

from django.db.models import SET_NULL
from django.utils import timezone
from django.contrib.auth.models import User


class Product(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    name = models.CharField(max_length=150)
    price = models.FloatField(null=False)
    description = models.CharField(max_length=1000)
    path = models.CharField(max_length=50, null=True)


class Offers(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    p_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(null=True)
    available = models.IntegerField(null=False)


class Order(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    o_id = models.ForeignKey(Offers, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    buyer_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    pieces = models.IntegerField( null=False)
    total = models.FloatField(null=False, default=0.0)
    city = models.CharField(max_length=50, null=True)
    street = models.CharField(max_length=50, null=True)
    number = models.CharField(max_length=10, null=True)
    zipcode = models.CharField(max_length=6, null=True)

class UserAddresses(models.Model):
    id = models.BigAutoField(primary_key=True, null=False),
    u_id = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    number = models.CharField(max_length=10)
    zipcode = models.CharField(max_length=6)