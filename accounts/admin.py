from django.contrib import admin
from .models import *

admin.site.register(CustomerAddress)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['email','username','is_staff','is_superuser','password']
    empty_value_display = 'is null'
    list_filter = ['email']
    list_per_page = 2
    search_fields = ('email',)
    fieldsets = (
            (None, {
                "fields": (
                    'email','password'
                ),
            }),
            ('personal info', {
                "description": 'This is personal information :)',
                "classes": ('collapse',),
                "fields": (
                    'date_joined',
                ),
                }
            ),
        )

@admin.register(Admin)
class CustomAdmin(admin.ModelAdmin):
    model = Admin
    list_display = ['email','username','is_staff','is_superuser']
    empty_value_display = 'is null'
    list_filter = ['email']
    list_per_page = 2
    search_fields = ('email',)
    fieldsets = (
            (None, {
                "fields": (
                    'username','email','password'
                ),
            }),
        )
    def get_queryset(self, request):
        return Admin.objects.filter(is_superuser = True,is_staff=True)   #CustomUser instead of Admin?

@admin.register(RestaurantManager)
class CustomRestaurantManager(admin.ModelAdmin):
    model = RestaurantManager
    list_display = ['email','username','is_staff','is_superuser']
    empty_value_display = 'is null'
    list_filter = ['email']
    list_per_page = 2
    search_fields = ('email',)
    fieldsets = (
            (None, {
                "fields": (
                    'username','email','password',
                ),
            }),
        )
    def get_queryset(self, request):
        return RestaurantManager.objects.filter(is_staff = True,is_superuser = False)

    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data["password"])
        obj.save()

class AddressInline(admin.TabularInline):
    model = Address.customer.through
    
@admin.register(Customer)
class CustomCustomer(admin.ModelAdmin):
    inlines = [AddressInline]
    model = Customer
    list_display = ['email','username','is_staff','is_superuser']
    empty_value_display = 'is null'
    list_filter = ['email']
    list_per_page = 2
    search_fields = ('email',)
    fieldsets = (
            (None, {
                "fields": (
                    'username','email','password',
                ),
            }),
        )
    def get_queryset(self, request):
        return Customer.objects.filter(is_staff = False,is_superuser = False)
    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data["password"])
        obj.save()    

@admin.register(Address)
class CustomAddress(admin.ModelAdmin):
    model = Address
    list_display = ['state','city','street','id']
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