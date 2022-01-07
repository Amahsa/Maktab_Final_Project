from django.contrib import admin
from .models import *


class Branchs(admin.TabularInline):
    model = Branch
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name','test']
    inlines = [Branchs]

    @admin.display(description='branchs')
    def test(self,object):
        return '|'.join([item.name for item in object.branchs.all()])




admin.site.register(Category)


admin.site.register(Status)

admin.site.register(Food)
admin.site.register(Meal)

class OrderItemss(admin.TabularInline):
    model = OrderItem
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['costumer','status' , 'created_at' , 'created_at_jalali']
    inlines = [OrderItemss]

    # @admin.display(description='order items')
    # def test(self,object):
    #     return '|'.join([item.name for item in object..all()])
    

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['restaurant','name' , 'category']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = [ 'branch','food','price', 'description']

    @admin.display(description='food')
    def food(self,object):
        return ' | '.join([item.name for item in object.food.all()])
    
@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order','order_count', 'food']

class MenuItems(admin.TabularInline):
    model = MenuItem
