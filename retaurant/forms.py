from .models import Food,Category,Meal
from django import forms
import datetime
from django.contrib.admin.widgets import AdminDateWidget

# class AddFoodForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(AddFoodForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'
    
#     Scheduling = forms.DateField(widget = forms.SelectDateWidget())


#     class Meta:
#         model = Task
#         fields = ("__all__")
#         widgets = {
#           'description': forms.Textarea(attrs={'rows':2, 'cols':25}),
#         }


class AddFoodForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = ("__all__")

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("__all__")

class AddMealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ("__all__")
