from django.urls import path
from .views import *



urlpatterns=[
    #websitemanager
    path('foods/',FoodView.as_view(),name="foods"),
    path('',show_foods,name="home"),
    path('food_form/',FoodCreate.as_view(),name='add_food'),
    path('delete_food/<int:pk>/', FoodDelete.as_view(), name='delete_food'),
    path('edit_food/<int:pk>/', FoodUpdate.as_view(), name='edit_food'),
    path('food_category/add/', PostFoodCategoryCreate.as_view(), name='add_food_category'),

    #cart
    path('cart/', cart, name="add_to_cart"),
    path('delete_orderitem/<int:pk>/',OrderItemDeleteView.as_view(),name="delete_orderitem"),
    path('orders_detail/<int:pk>/',food,name="order_detail"),

    #restaurant
    


    path('restaurant_panel',ManagerMenus.as_view(),name="restaurant_panel"),
    path("create_menu/",MenuCreate.as_view(),name="create_menu"),
    path("delete_menu/<int:pk>/",MenuDelete.as_view(),name="delete_menu"),
    path("edit_menu/<int:pk>/",MenuUpdate.as_view(),name="edit_menu"),


    # search
    path('search/',search,name="search"),


    #customer
    path('customer_panel/',CustomerOrders.as_view(),name="customer_panel"),

    
    ]