from django.contrib import admin
from .models import Product, Offers, Order
from django.utils import timezone


admin.site.register(Product)
admin.site.register(Offers)
admin.site.register(Order)
