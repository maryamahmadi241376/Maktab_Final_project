from django.urls import path

from .views import ManagerCreate,CustomerCreate,AddressCreate,managers_signup

urlpatterns = [
    
    path('managers_signup/',managers_signup,name="managers_signup"),
    # path('add_admin/',AdminCreate.as_view(),name = 'add_admin'),
    path('add_manager/',ManagerCreate.as_view(),name = 'add_manager'),
    path('add_customer/',AddressCreate.as_view(),name = 'add_address'),
    path('customer/',CustomerCreate.as_view(),name = 'add_customer'),
    
]