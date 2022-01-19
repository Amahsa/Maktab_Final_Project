from django.shortcuts import render
from ..models import Food
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView
from ..forms import AddFoodForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import site_admin_required


@method_decorator([login_required, site_admin_required], name='dispatch')
class FoodList(ListView):
    model = Food

@method_decorator([login_required, site_admin_required], name='dispatch')
class AddFoodView(CreateView):
    form_class = AddFoodForm
    success_url = reverse_lazy('foods_list')
    template_name = 'manager/add_food.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class FoodDetailView(DetailView):
    model = Food
    template_name = 'manager/food_detail.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class FoodUpdateView(UpdateView):
    model = Food
    template_name = 'manager/food_edit.html'
    fields = ['name','category','meal']
    success_url = reverse_lazy('foods_list')

@method_decorator([login_required, site_admin_required], name='dispatch')
class FoodDeleteView(DeleteView):
    model = Food
    template_name = 'manager/food_delete.html'
    success_url = reverse_lazy('foods_list')



    

