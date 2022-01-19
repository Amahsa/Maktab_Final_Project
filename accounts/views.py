from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy,reverse
from django.views import generic

from .forms import *
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from accounts.mixins import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin 
from django.views.generic import ListView, DetailView,CreateView 
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from accounts.models import CustomerAddress, Customer,Admin
from django.views import View



class SignUpView(generic.CreateView):
    form_class = CustomUserSignUpForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

class AdminSignUpView(generic.CreateView):
       
    form_class = AdminSignUpForm
    success_url = reverse_lazy('home')
    template_name = 'account/signup.html'

    def form_valid(self, form):

        user = form.save()
        # login(self.request, user)
        return super().form_valid(form)

class HomePageView(LoginRequiredMixin, TemplateView): 
    template_name = 'home.html'


# class AdminSignUpView(View):
#     def get(self, request):
#         return render (request, 'site_admin_signup.html')
        


#     def post(self, request):

#         postData = request.POST

#         first_name = postData.get ('firstname')
#         last_name = postData.get ('lastname')
#         phone = postData.get ('phone')
#         email = postData.get ('email')
#         password = postData.get ('password')
#         # validation
#         value = {
#             'first_name': first_name,
#             'last_name': last_name,
#             'phone': phone,
#             'email': email
#         }
#         error_message = None

#         admin =  Admin(first_name=first_name,
#                              last_name=last_name,
#                              username=email,
#                              phone_number=phone,
#                              email=email,
#                              password=password)


#         error_message = self.validateAdmin (admin)

#         #------------------------------
        
#         if not error_message:
#             print (first_name, last_name, phone, email, password)
#             admin.password = make_password (admin.password)
#             admin.save ()

#             data = {
#                 'error': error_message,
#                 'values': value
#             }
                 
#             return render (request, 'site_dmin_signup.html', data)
#         else:
#             data = {
#                 'error': error_message,
#                 'values': value
#             }
#             return render (request, 'site_dmin_signup.html', data)

#     def validateCustomer(self, customer):
#         error_message = None
#         if (not customer.first_name):
#             error_message = "Please Enter your First Name !!"
#         elif len (customer.first_name) < 3:
#             error_message = 'First Name must be 3 char long or more'
#         elif not customer.last_name:
#             error_message = 'Please Enter your Last Name'
#         elif len (customer.last_name) < 3:
#             error_message = 'Last Name must be 3 char long or more'
#         elif not customer.phone_number:
#             error_message = 'Enter your Phone Number'
#         elif len (customer.phone_number) < 10:
#             error_message = 'Phone Number must be 10 char Long'
#         elif len (customer.password) < 5:
#             error_message = 'Password must be 5 char long'
#         elif len (customer.email) < 5:
#             error_message = 'Email must be 5 char long'
#         elif customer.isExists ():
#             error_message = 'Email Address Already Registered..'
#         return error_message

