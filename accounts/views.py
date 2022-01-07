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


