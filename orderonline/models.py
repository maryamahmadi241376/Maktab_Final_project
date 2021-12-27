from django.db import models
from django.core.validators import MinValueValidator

class Order(models.Model):
    customer = models.ForeignKey('accounts.Customer',on_delete=models.CASCADE,related_name="customer_order")
    customer_address = models.OneToOneField('accounts.Address',on_delete=models.CASCADE,related_name="orders")
    # BRANCHSTATUS = [('confirm','confirm'),('is_sending','is_sending'),('is_delivered','is_delivered')]
    # branch_status = models.CharField(choices=BRANCHSTATUS,default="-----",max_length=13)
    CUSTOMERSTATUS = [('ordered','ordered'),('order_confirmed','order_confirmed'),('is_sending','is_sending'),('delivered','delivered')]
    customer_status = models.CharField(choices=CUSTOMERSTATUS,default="-----",max_length=16)
    order_number = models.IntegerField(validators = [MinValueValidator(1)])
    delivery_time = models.TimeField(auto_now_add=True)
    order_date = models.DateField(auto_now_add=True)
    food = models.ManyToManyField('Food',related_name='order')
    branch = models.ForeignKey('RestaurantBranch',related_name="delivery",on_delete=models.CASCADE)
    
    def __str__(self):
        return self.status

class Food(models.Model):
    food_name = models.CharField(max_length=200,verbose_name="food_name")
    food_category_id = models.ForeignKey("FoodCategory",on_delete=models.CASCADE,related_name="menues")
    food_image = models.ImageField(upload_to = 'media/')  #setting and url not complete
    food_description = models.TextField(max_length=1000,default="",verbose_name="food_description",null = True,blank=True)
    food_created_date = models.DateField(auto_now_add=True)
    meal = models.ManyToManyField('MealCategory',related_name="meal_menues")

    def __str__(self):
        return self.food_name

class FoodCategory(models.Model):
    food_category_name = models.CharField(max_length=200,verbose_name="food_category_name")

    def __str__(self):
        return self.food_category_name

class MealCategory(models.Model):
    meal_category_name = models.CharField(max_length=200,verbose_name="meal_category_name")

    def __str__(self):
        return self.meal_category_name

class Menu(models.Model):   #middle table
    food = models.ManyToManyField(Food,related_name="food_menu")
    price = models.IntegerField()
    number = models.IntegerField()

    def __str__(self):
        return f"food id : {self.food}"

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=200,verbose_name="restaurant_name")

    def __str__(self):
            return self.restaurant_name


class RestaurantBranch(Restaurant):
    food_category = models.OneToOneField(FoodCategory,on_delete=models.CASCADE,related_name='branch')
    restaurant_id = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="restaurant_branchs")
    restaurant_branch_name = models.CharField(max_length=200,verbose_name="restaurant_branch_name")
    address = models.OneToOneField('accounts.Address',on_delete=models.CASCADE,related_name='restaurantbranchs')
    restaurant_branch_description = models.TextField(max_length=1000,default="",verbose_name="restaurant_branch_description",blank=True,null=True)
    restaurant_branch_created_date = models.DateField(auto_now_add=True)
    restaurant_branch_status = models.BooleanField('active',default=True)
    manager = models.OneToOneField('accounts.RestaurantManager',on_delete=models.CASCADE,related_name='branchs')
    menu = models.OneToOneField(Menu,on_delete=models.CASCADE,related_name="branch_menus")

    def __str__(self):
        return self.restaurant_branch_name

