from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin 
from .forms import *
from .models import *

class CustomUserAdmin(admin.ModelAdmin): 
    add_form = CustomUserSignUpForm 
    form = CustomUserChangeForm 
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_site_admin','is_customer','is_restaurant_manager']


    fields = ['email', 'username', 'is_staff', 'is_site_admin','is_customer','is_restaurant_manager' ]
    

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # add_form = CustomUserSignUpForm 
    # form = CustomUserChangeForm 
    list_display = ['id', 'username', 'email']
    exclude = ('address',)
    # fields = ['id', 'username', 'email' , '']
    # fields = ['email', 'username','is_staff', 'is_site_admin','is_customer','is_restaurant_manager' ]

    list_display_links = ['username','email']
    # list_editable = ['age', 'email']
    search_fields = ['username', 'email']

    def get_queryset(self, request):
        return Customer.objects.filter(is_customer=True)


@admin.register(Manager)
class ManagerProxyAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']
    # fields = ['username', 'email']
    list_display_links = ['username']
    # list_editable = ['age', 'email']
    search_fields = ['username', 'email']


    def get_queryset(self, request):
        return CustomUser.objects.filter(is_restaurant_manager=True)


@admin.register(Admin)
class AdminProxyAdmin(admin.ModelAdmin):
    add_form = AdminSignUpForm 
    form = AdminChangeForm 

    list_display = ['id', 'username', 'email']
    # fields = ['id', 'username', 'email']
    list_display_links = ['username']
    # list_editable = ['age', 'email']
    search_fields = ['username', 'email']

    def get_queryset(self, request):
        return CustomUser.objects.filter(is_site_admin=True)

admin.site.register(Address)
admin.site.register(CustomerAddress)