from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models import fields
from django.db.models.deletion import CASCADE


# --------------------------------------------------
class Address(models.Model):
    state_Choices=(
        ('تهران','تهران'),
        ('اصفهان','اصفهان'),
        ('شیراز','شیراز'),
        ('مشهد','مشهد')    
    ) 

    city_Choices=(
        ('قدس','قدس'),
        ('اسلام شهر','اسلام شهر'),   
    ) 
    state=models.CharField(max_length=100,default='',choices=state_Choices)
    city = models.CharField(max_length=100,default='')
    full_address = models.CharField(max_length=500,default='')


    def __str__(self):
        return f'{self.state} {self.city} {self.full_address}'

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"

class CustomerAddress(models.Model):
    # state_Choices=(
    #     ('تهران','تهران'),
    #     ('اصفهان','اصفهان'),
    #     ('شیراز','شیراز'),
    #     ('مشهد','مشهد')    
    # ) 

    # city_Choices=(
    #     ('قدس','قدس'),
    #     ('اسلام شهر','اسلام شهر'),   
    # ) 
    state = models.CharField(max_length=100,default='Tehran')
    city = models.CharField(max_length=100,default='Tehran')
    full_address = models.CharField(max_length=500,default='Azadi')
    customer = models.ForeignKey('Customer',on_delete=CASCADE,related_name='customer_addresses')


    def __str__(self):
        return f'{self.state} {self.city} {self.full_address}'

    class Meta:
        verbose_name = "آدرس مشتری"
        verbose_name_plural = "آدرس های مشتریان"


#-----------------------------------------------------
class CustomUser(AbstractUser):

    is_site_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_restaurant_manager = models.BooleanField(default=False)


    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+989123456789'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True , null=True)
    

#--------------------------------------------------
class Customer(CustomUser):
    address = models.ManyToManyField(Address)
    fields = ['email','address','phone_number']
    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"
    def save(self,*args,**kwargs):
        if not self.id :
            self.is_customer  = True
        super().save(*args,**kwargs)
    

    #to save the data
    def register(self):
        self.save()


    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email= email)
        except:
            return False


    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return False

        
        
#--------------------------------------------------

class Manager(CustomUser):
    fields = ['email']
    CustomUser.is_staff = True
    CustomUser.is_site_admin = True
    # AbstractUser.is_staff = True

    class Meta:
        proxy = True
        verbose_name: "مدیر رستوران"
        verbose_name_plural = 'مدیران رستوران ها'
    def save(self,*args,**kwargs):
        if not self.id :
            self.is_restaurant_manager = True
        super().save(*args,**kwargs)

#--------------------------------------------------
class Admin(CustomUser):   
    fields = ['email'] 
    class Meta:
        proxy = True
        verbose_name: 'ادمین'
        verbose_name_plural = 'ادمین ها'
    def save(self,*args,**kwargs):
        if not self.id :
            self.is_site_admin  = True
        super().save(*args,**kwargs)


