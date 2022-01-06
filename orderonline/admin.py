from django.contrib import admin
from .models import *

admin.site.register(Restaurant)
admin.site.register(MealCategory)
admin.site.register(FoodCategory)
admin.site.register(Menu)






@admin.register(RestaurantBranch)
class CustomRestaurantBranch(admin.ModelAdmin):
    model = RestaurantBranch
    list_display = ['restaurant_branch_name','address','restaurant_branch_status',]
    list_editable = ['restaurant_branch_status',]
    empty_value_display = 'is null'
    list_filter = ['restaurant_branch_name','address','restaurant_branch_status',]
    list_per_page = 4
    search_fields = ['restaurant_branch_name','address','restaurant_branch_status',]

@admin.register(OrderItem)
class CustomMenu(admin.ModelAdmin):
    model = OrderItem
    list_display = ['number',]
    empty_value_display = 'is null'
    list_per_page = 4
    search_fields = ['number',]
    fieldsets = (
            (None, {
                "fields": (
                    'order','menu','number',
                ),
            }),
        )

@admin.register(Food)
class CustomFood(admin.ModelAdmin):
    model = Food
    list_display = ['food_name','food_image','food_description',]
    list_editable = ['food_description',]
    empty_value_display = 'is null'
    list_filter = ['food_name',]
    list_per_page = 4
    search_fields = ['food_name',]
    fieldsets = (
            (None, {
                "fields": (
                    'food_name','food_image','food_category_id',
                ),
            }),
            ('personal info', {
                "description": 'This is food information :)',
                "classes": ('collapse',),
                "fields": (
                    'food_description',
                ),
                }
            ),
        )

@admin.register(Order)
class CustomOrder(admin.ModelAdmin):
    model = Order
    list_display = ['delivery_time','customer_status',]
    list_editable = ['customer_status',]
    empty_value_display = 'is null'
    list_filter = ['customer_status',]
    list_per_page = 4
    search_fields = ['delivery_time','customer_status',]
    fieldsets = (
            (None, {
                "fields": (
                    'order_item','total_price','customer','address','branch','customer_status',
                ),
            }),
        )