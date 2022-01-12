from django.urls import path

from .views import *

urlpatterns = [
    
    # path('managers_signup/',managers_signup,name="managers_signup"),
    # path('add_admin/',AdminCreate.as_view(),name = 'add_admin'),
    
    #customer
    # path('add_customer/',AddressCreate.as_view(),name = 'add_address'),
    path('customer/',customer_signup,name = 'add_customer'),
    path('customeredit/<int:pk>/',CustomerEdit.as_view(),name="customer_edit"),
    path('signout/<int:pk>/',CustomerSignOut.as_view(),name="customer_signout"),

    #address
    path('change_main_address/<int:pk>/',change_main_address,name="change_main_address"),
    path('delete_address/<int:pk>/',delete_address,name="delete_address"),
    path('address/',address_create,name = "addaddress"),
    

    #manager
    path('branch_edit/<int:pk>/',BranchManagerEdit.as_view(),name="branch_edit"),
    path('manager_edit/<int:pk>/',ManagerEdit.as_view(),name="manager_edit"),
    path('manager_signup/',manager_signup,name="add_manager"),

]