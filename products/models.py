from django.db import models
from categories.models import Category

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    availableQuantity = models.IntegerField()
    category = models.ForeignKey(
        to=Category, 
        on_delete=models.CASCADE
    )
    

class ProductImage(models.Model):
    fileName = models.CharField(max_length=255)
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE
    )
