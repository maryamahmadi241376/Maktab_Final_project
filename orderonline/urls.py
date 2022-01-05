from django.urls import path
from .views import *



urlpatterns=[
    
    path('foods/',foodView,name="foods"),
    path('',show_foods,name="home"),
    # path('food_form/',FoodCreate.as_view(),name='add_food'),
    # path('delete_food/<int:pk>/', FoodDelete.as_view(), name='delete_food'),
    # path('edit_food/<int:pk>/', FoodUpdate.as_view(), name='edit_food'),
    # path('food_category/add/', PostFoodCategoryCreate.as_view(), name='add_food_category'),
    # path('cart/', cart, name="add_to_cart"),
    # path('delete_orderitem/<int:pk>/',OrderItemDeleteView.as_view(),name="delete_orderitem"),
    # path('orders_detail/<int:pk>/',food,name="order_detail"),
    # # path('food_form/',addfood,name='add_food'),
    # path("address/",AddressView.as_view(),name="address")
    ]