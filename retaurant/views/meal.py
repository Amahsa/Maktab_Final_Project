from django.db.models import fields
from django.shortcuts import render
from django.views.generic import DetailView,ListView,CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView, UpdateView

from ..decorators import site_admin_required
from ..models import Meal
from ..forms import AddMealForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..decorators import site_admin_required


@method_decorator([login_required, site_admin_required], name='dispatch')
class MealList(ListView):
    model = Meal

@method_decorator([login_required, site_admin_required], name='dispatch')
class AddMealView(CreateView):
    form_class = AddMealForm
    success_url = reverse_lazy('meals_list')
    template_name = 'manager/add_meal.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class DeleteMealView(DeleteView):
    model = Meal
    success_url = reverse_lazy('meals_list')
    template_name = 'manager/delete_meal.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class MealUpdateView(UpdateView):
    model = Meal
    fields=('name',)
    success_url = reverse_lazy('meals_list')
    template_name = 'manager/meal_edit.html'  
