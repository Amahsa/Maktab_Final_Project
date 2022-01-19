from django.db.models import fields
from django.shortcuts import render
from django.views.generic.edit import DeleteView, UpdateView
from ..models import Category, Food
from django.views.generic import DetailView,ListView,CreateView,DeleteView
from ..forms import AddCategoryForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import site_admin_required


@method_decorator([login_required, site_admin_required], name='dispatch')
class CategoryList(ListView):
    model = Category
    template_name = 'manager/catogory_list.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class AddCategoryView(CreateView):
    form_class = AddCategoryForm
    success_url = reverse_lazy('category_list')
    template_name = 'manager/add_category.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class DeleteCategoryView(DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')
    template_name = 'manager/delete_category.html'
    
@method_decorator([login_required, site_admin_required], name='dispatch')
class CategoryEditView(UpdateView):
    model = Category
    fields=('name',)
    success_url = reverse_lazy('category_list')
    template_name = 'manager/category_edit.html'
