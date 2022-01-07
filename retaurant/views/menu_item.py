from django.shortcuts import render
from ..models import MenuItem
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView
from ..forms import AddFoodForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from ..decorators import site_admin_required

@method_decorator([login_required, site_admin_required], name='dispatch')
class MenuItemList(ListView):
    model = MenuItem

def get_branch_menu(req,pk):
    menu = MenuItem.objects.filter(branch=pk)
    return render(req,'retaurant/restaurant.html',context={'products' : menu})







# class MenuItemList(ListView):
#     model = MenuItem
#     template_name = ''

#     def get_queryset(self) -> QuerySet[T]:
#         return super().get_queryset()

# @method_decorator([login_required, site_admin_required], name='dispatch')
# class AddFoodView(CreateView):
#     form_class = AddFoodForm
#     success_url = reverse_lazy('foods_list')
#     template_name = 'retaurant/add_food.html'


# class FoodDetailView(DetailView):
#     model = Food
#     template_name = 'food_detail.html'

# class FoodUpdateView(UpdateView):
#     model = Food
#     template_name = 'food_edit.html'
#     fields = ['name', 'meal', 'category']

# class FoodDeleteView(DeleteView): # new
#     model = Food
#     template_name = 'food_delete.html'
#     success_url = reverse_lazy('foods_list')
    

