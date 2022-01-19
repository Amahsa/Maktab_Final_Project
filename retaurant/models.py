from django.db import models
from django.db.models import manager
from django.db.models.base import Model
from django.db.models.enums import Choices
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import *
from django.core.validators import MaxLengthValidator
import os
from datetime import datetime
import jdatetime

class Restaurant(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "رستوران"
        verbose_name_plural = "رستوران ها"
    
class Category(models.Model): # *************

    name = models.CharField(max_length = 200, unique=True, default='Traditional')
    def __str__(self):
            return self.name
    
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    

class Branch(models.Model):
    address = models.ForeignKey(Address, on_delete= models.CASCADE)
    name = models.CharField(max_length = 200)
    registered_at=models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name= 'category_branchs')
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE , related_name='branchs')
    manager = models.ForeignKey(Manager,on_delete=models.CASCADE,related_name='manager_branch')


    def __str__(self):
        return f'{self.restaurant.name} {self.name}'
    class Meta:
        verbose_name = "شعبه"
        verbose_name_plural = "شعبات"

    
    @staticmethod
    def get_all_branches():
        return Branch.objects.all()
    
    @staticmethod
    def get_branche_by_manager_email(email):
        return Branch.objects.get(manager=Manager.objects.get(email=email))

    @staticmethod
    def get_branches_by_category(category_id):
        if category_id:
            return Branch.objects.filter(category=category_id) 
        else:
            return Branch.get_all_branches();

   
class MenuItem(models.Model):
    def get_upload_path(self,file_name):
        ext = file_name.split('.')[-1]
        filename = '{}.{}'.format(str(self.id),ext)
        path = 'Foods'
        return os.path.join(path,filename)

    branch = models.ForeignKey(Branch,related_name='menu_items',on_delete=models.CASCADE)
    food = models.ForeignKey('Food', related_name='menu_foods' , on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=0) # ToDo
    description = models.TextField(blank=True, null=True)
    count = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to = get_upload_path) 

    def __str__(self):
            return f'{self.food.name} {self.branch}'
    
    class Meta:
        verbose_name = "آیتم منو"
        verbose_name_plural = "آیتم های منو"

    @staticmethod
    def get_products_by_id(ids): # list(id) -> list(MenueItem_objects)
        return MenuItem.objects.filter (id__in=ids)

    @staticmethod
    def get_all_products(): 
        return MenuItem.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return MenuItem.objects.filter(food__category=category_id) # test 
        else: 
            return MenuItem.get_all_products();

    @staticmethod
    def get_all_products_by_branch_id(branch_id):
        if branch_id:
            return MenuItem.objects.filter(branch=branch_id) # test
        else:
            return MenuItem.get_all_products();

class Food(models.Model):

    
    class Meta:
        verbose_name = "غذا"
        verbose_name_plural = "غذا ها"


    name = models.CharField(max_length=200)    
    created_at = models.DateTimeField(auto_now_add=True)
    meal = models.ManyToManyField('Meal' , related_name='meals_food')
    category = models.ManyToManyField(Category , related_name='categories_food')

    def __str__(self):
            return self.name 
    
    @property
    def created_at_jalali(self):
        jalali_date = jdatetime.datetime.fromgregorian(datetime=self.created_at)
        return jalali_date

class Meal(models.Model):
    name = models.CharField(max_length=200 ,unique=True)

    def __str__(self):
            return self.name 
    
    class Meta:
        verbose_name = "وعده غذایی"
        verbose_name_plural = "وعده های غذایی"


class Order(models.Model):
    costumer = models.ForeignKey(Customer,related_name='customer_orders' ,on_delete=models.CASCADE)
    address = models.CharField(max_length=600, default='تهران،تهران،خیابان آزادی')
    # OneToOneField(Address ,on_delete=models.CASCADE)
    status = models.ForeignKey('Status',related_name='status_orders' ,on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=0 , default= 100000) # ******** مینیوم
    
    def __str__(self):
            return f'{self.costumer}'
    
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"
    
    @property
    def created_at_jalali(self):
        jalali_date = jdatetime.datetime.fromgregorian(datetime=self.created_at)
        return jalali_date
    
    
    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(costumer_id):
        return Order.objects.filter(costumer=costumer_id).order_by('-created_at')
    
    # @staticmethod
    # def get_orders_branch(costumer_id):
    #     return Order.objects.filter(costumer=costumer_id).order_by('-created_at')


class Status(models.Model): # ***********
    status = models.CharField(max_length=200)
    
    def __str__(self):
            return self.status 
    
    class Meta:
        # proxy = True
        verbose_name = "وضعیت سفارش"
        verbose_name_plural = "وضعیت های سفارش"


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete= models.DO_NOTHING,null=True,related_name='order_items')
    food = models.ForeignKey(MenuItem,related_name='food_order_items' , on_delete=models.CASCADE)
    order_count = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم های  سفارش"
    
    def __str__(self):
            return f'سفارش  : {self.order.id}'

    @staticmethod
    def get_order_items_by_order_id(order_id):
        return OrderItem.objects.filter(order=order_id)
