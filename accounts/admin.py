from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email','username','is_staff','is_superuser']
    list_editable = ['username',]
    empty_value_display = 'is null'
    list_filter = ['first_name','email','date_joined',]
    list_per_page = 2
    search_fields = ('username','email')
    date_directly = ['date_joined']
    fieldsets = (
            (None, {
                "fields": (
                    'email','username'
                ),
            }),
            ('personal info', {
                "description": 'This is personal information :)',
                "classes": ('collapse',),
                "fields": (
                    'first_name','last_name','date_joined'
                ),
                }
            ),
        )

@admin.register(Admin)
class CustomAdmin(UserAdmin):
    model = Admin
    list_display = ['email','username','is_staff','is_superuser']
    list_editable = ['username',]
    empty_value_display = 'is null'
    list_filter = ['first_name','email','date_joined',]
    list_per_page = 2
    search_fields = ('username','email')
    date_directly = ['date_joined']
    fieldsets = (
            (None, {
                "fields": (
                    'email','username'
                ),
            }),
            ('personal info', {
                "description": 'This is personal information :)',
                "classes": ('collapse',),
                "fields": (
                    'first_name','last_name','date_joined'
                ),
                }
            ),
        )
    def get_queryset(self, request):
        return Customer.objects.filter(is_superuser = True)

@admin.register(RestaurantManager)
class CustomRestaurantManager(UserAdmin):
    model = RestaurantManager
    list_display = ['email','username','is_staff','is_superuser']
    list_editable = ['username',]
    empty_value_display = 'is null'
    list_filter = ['first_name','email','date_joined',]
    list_per_page = 2
    search_fields = ('username','email')
    date_directly = ['date_joined']
    fieldsets = (
            (None, {
                "fields": (
                    'email','username'
                ),
            }),
            ('personal info', {
                "description": 'This is personal information :)',
                "classes": ('collapse',),
                "fields": (
                    'first_name','last_name','date_joined'
                ),
                }
            ),
        )
    def get_queryset(self, request):
        return Customer.objects.filter(is_staff = True)

class AddressInline(admin.TabularInline):
    model = Address.customer.through
    
@admin.register(Customer)
class CustomCustomer(UserAdmin):
    inlines = [AddressInline]
    model = Customer
    list_display = ['email','username','is_staff','is_superuser']
    list_editable = ['username',]
    empty_value_display = 'is null'
    list_filter = ['first_name','email','date_joined',]
    list_per_page = 2
    search_fields = ('username','email')
    date_directly = ['date_joined']
    fieldsets = (
            (None, {
                "fields": (
                    'email','username'
                ),
            }),
            ('personal info', {
                "description": 'This is personal information :)',
                "classes": ('collapse',),
                "fields": (
                    'first_name','last_name','date_joined'
                ),
                }
            ),
        )
    def get_queryset(self, request):
        return Customer.objects.filter(is_staff = False)

@admin.register(Address)
class CustomAddress(admin.ModelAdmin):
    model = Address
    list_display = ['state','city','street']
    list_editable = ['street',]
    empty_value_display = 'is null'
    list_filter = ['state','city','street',]
    list_per_page = 2
    search_fields = ('state','city')
    fieldsets = (
            (None, {
                "fields": (
                    'state','city'
                ),
            }),
            ('personal info', {
                "description": 'This is personal information :)',
                "classes": ('collapse',),
                "fields": (
                    'street','pluque'
                ),
                }
            ),
        )