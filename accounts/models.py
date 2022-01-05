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

    def save(self,*args, **kwargs):
        if not self.id:
            self.is_staff = True
            self.is_superuser = True
        super(Admin,self).save(*args, **kwargs)

class RestaurantManager(CustomUser):
    class Meta:
        proxy = True
        verbose_name = "RestaurantManager"

    def save(self,*args, **kwargs):
        if not self.id:
            self.is_staff = True
            self.is_superuser = False
        super(RestaurantManager,self).save(*args, **kwargs)

class Customer(CustomUser):
    address = models.ManyToManyField('Address',related_name='customer')
    customer_status = models.BooleanField('block',default=False)
    device = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Customer"
    
    def save(self,*args, **kwargs):
        if not self.id:
            self.is_staff = False
            self.is_superuser = False
        super(Customer,self).save(*args, **kwargs)

class Address(models.Model):
    is_main_address = models.BooleanField(default=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=30)
    pluque = models.IntegerField(validators = [MinValueValidator(1)])
    
    def __str__(self):
        return self.state+","+self.city+","+self.street