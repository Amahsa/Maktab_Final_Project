from pyexpat import model
from django.shortcuts import render

# from SRC.accounts.models import Manager
from ..models import Branch, Food,Customer,Restaurant,MenuItem,Category,Meal
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView
from ..forms import AddFoodForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import site_admin_required
from django.utils.decorators import method_decorator
from ..decorators import *
import operator
from ..forms import *
from accounts.models import Manager


@method_decorator([login_required, site_admin_required], name='dispatch')
class FoodList(ListView):
    model = Food
    template_name = 'restaurant/admin/food/food_list.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class AddFoodView(CreateView):
    form_class = AddFoodForm
    success_url = reverse_lazy('food_list')
    template_name = 'restaurant/admin/food/add_food.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class FoodDetailView(DetailView):
    model = Food
    template_name = 'restaurant/admin/food/food_detail.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class FoodUpdateView(UpdateView):
    model = Food
    template_name = 'restaurant/admin/food/food_edit.html'
    fields = ['name','category','meal']
    success_url = reverse_lazy('food_list')

@method_decorator([login_required, site_admin_required], name='dispatch')
class FoodDeleteView(DeleteView):
    model = Food
    template_name = 'restaurant/admin/food/food_delete.html'
    success_url = reverse_lazy('food_list')


@method_decorator([login_required, site_admin_required], name='dispatch')
class CustomerList(ListView):
    model = Customer
    template_name = 'restaurant/admin/customer/customer_list.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'restaurant/admin/customer/customer_detail.html'



@method_decorator([login_required, site_admin_required], name='dispatch')
class CustomerUpdateView(UpdateView):
    model = Customer
    fields = [
        "first_name",
        "last_name",
    ]
    template_name = 'restaurant/admin/customer/customer_edit.html'
    success_url = reverse_lazy('customer_list')
    
@method_decorator([login_required, site_admin_required], name='dispatch')
class CustomerDeleteView(DeleteView): 
    model = Customer
    template_name = 'restaurant/admin/customer/customer_delete.html'
    success_url = reverse_lazy('customer_list')


# -------------------------------------------------
@method_decorator([login_required, site_admin_required], name='dispatch')
class RestaurantList(ListView):
    model = Restaurant
    template_name = 'restaurant/admin/restaurant/restaurant_list.html'

# -------------------------------------------------
@method_decorator([login_required, site_admin_required], name='dispatch')
class RestaurantDeleteView(DeleteView):
    model = Restaurant
    success_url = reverse_lazy('restaurant_list')
    template_name = 'restaurant/admin/restaurant/delete_restaurant.html'
# -------------------------------------------------
@method_decorator([login_required, site_admin_required], name='dispatch')
class RestaurantUpdateView(UpdateView):
    model = Restaurant
    template_name = 'restaurant/admin/restaurant/restaurant_edit.html'
    fields = ['name',]
    success_url = reverse_lazy('restaurant_list')

# -------------------------------------------------  
# @method_decorator([login_required, site_admin_required], name='dispatch')
@login_required
@user_passes_test(operator.attrgetter('is_site_admin'), 
login_url='/login',redirect_field_name='login')
def restaurant_branches(request,pk):
   
    mydictionary = {
        "branch" : Branch.objects.get(pk=pk),
    }
    return render(request,'restaurant/admin/restaurant/restaurant_branch.html',
    context=mydictionary)

@login_required
@user_passes_test(operator.attrgetter('is_site_admin'), 
login_url='/login',redirect_field_name='login')
def branch_menu(request,pk):
    branch = Branch.objects.get(pk=pk)
    food_list = MenuItem.objects.filter(branch=branch)
    category_list = Category.objects.all()
    return render(request,'restaurant/admin/restaurant/branch_menu.html',
    context={'food_list': food_list , 'categories' :category_list , 'branch':branch})

@method_decorator([login_required, site_admin_required], name='dispatch')
class BranchUpdateView(LoggedInRedirectMixin,UpdateView):
    model = Branch
    template_name = 'restaurant/admin/restaurant/branch_edit.html'
    fields = ['name','address','category']
    def get_success_url(self):
          companyid=self.kwargs['pk']
          return reverse_lazy('restaurant_branch', kwargs={'pk': companyid})

@method_decorator([login_required, site_admin_required], name='dispatch')
class BranchDeleteView(LoggedInRedirectMixin,ISAdminRedirectMixin,DeleteView):
    model = Branch
    template_name = 'restaurant/admin/restaurant/delete_branch.html'
    success_url = reverse_lazy('restaurant_list')
  

# ------------------------------------------------- 
@method_decorator([login_required, site_admin_required], name='dispatch')
class MealList(ListView):
    model = Meal
    template_name = 'restaurant/admin/meal/meal_list.html'
# ------------------------------------------------- 
@method_decorator([login_required, site_admin_required], name='dispatch')
class AddMealView(CreateView):
    form_class = AddMealForm
    success_url = reverse_lazy('meal_list')
    template_name = 'restaurant/admin/meal/add_meal.html'
# ------------------------------------------------- 
@method_decorator([login_required, site_admin_required], name='dispatch')
class DeleteMealView(DeleteView):
    model = Meal
    success_url = reverse_lazy('meal_list')
    template_name = 'restaurant/admin/meal/delete_meal.html'
# ------------------------------------------------- 
@method_decorator([login_required, site_admin_required], name='dispatch')
class MealUpdateView(UpdateView):
    model = Meal
    fields=('name',)
    success_url = reverse_lazy('meal_list')
    template_name = 'restaurant/admin/meal/meal_edit.html'  
# ------------------------------------------------- 


@method_decorator([login_required, site_admin_required], name='dispatch')
class CategoryList(ListView):
    model = Category
    template_name = 'restaurant/admin/category/catogory_list.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class AddCategoryView(CreateView):
    form_class = AddCategoryForm
    success_url = reverse_lazy('category_list')
    template_name = 'restaurant/admin/category/add_category.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class DeleteCategoryView(DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')
    template_name = 'restaurant/admin/category/delete_category.html'
    
@method_decorator([login_required, site_admin_required], name='dispatch')
class CategoryEditView(UpdateView):
    model = Category
    fields=('name',)
    success_url = reverse_lazy('category_list')
    template_name = 'restaurant/admin/category/category_edit.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class ManagerListView(ListView):
    model = Manager
    template_name = 'restaurant/admin/manager/manager_list.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class ManagerEditView(UpdateView):
    model = Manager
    fields=('first_name','last_name',)
    template_name = 'restaurant/admin/manager/manager_edit.html'
    success_url = reverse_lazy('manager_list')

@method_decorator([login_required, site_admin_required], name='dispatch')
class ManagerDeleteView(DeleteView):
    model = Manager
    success_url = reverse_lazy('manager_list')
    template_name = 'restaurant/admin/manager/delete_manager.html'
