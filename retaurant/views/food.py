from django.shortcuts import render
from ..models import Food
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView
from ..forms import AddFoodForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import site_admin_required

class FoodList(ListView):
    model = Food


@method_decorator([login_required, site_admin_required], name='dispatch')
class AddFoodView(CreateView):
    form_class = AddFoodForm
    success_url = reverse_lazy('foods_list')
    template_name = 'retaurant/add_food.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class FoodDetailView(DetailView):
    model = Food
    template_name = 'retaurant/food_detail.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class FoodUpdateView(UpdateView):
    model = Food
    template_name = 'retaurant/food_edit.html'
    fields = ['name', 'meal', 'category']

@method_decorator([login_required, site_admin_required], name='dispatch')
class FoodDeleteView(DeleteView):
    model = Food
    template_name = 'retaurant/food_delete.html'
    success_url = reverse_lazy('foods_list')



    

