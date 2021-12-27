from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Admin(CustomUser):
    class Meta:
        proxy = True
        verbose_name = "Admin"

class RestaurantManager(CustomUser):
    class Meta:
        proxy = True
        verbose_name = "RestaurantManager"

class Customer(CustomUser):
    address = models.ManyToManyField('Address',related_name='customer')
    class Meta:
        verbose_name = "Customer"

class Address(models.Model):
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=30)
    pluque = models.IntegerField(validators = [MinValueValidator(1)])
    
    def __str__(self):
        return self.state+","+self.city+","+self.street