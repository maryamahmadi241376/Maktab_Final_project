from django.contrib import admin
from .models import *

admin.site.register(RestaurantBranch)
admin.site.register(Food)
admin.site.register(Menu)
admin.site.register(Restaurant)
admin.site.register(MealCategory)
admin.site.register(FoodCategory)
admin.site.register(Order)