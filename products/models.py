from django.db import models
from categories.models import Category

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    availableQuantity = models.IntegerField()
    category = models.ForeignKey(
        to=Category, 
        on_delete=models.CASCADE
    )
