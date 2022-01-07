from django.urls import path
from .views import *
from django.views.generic import TemplateView,DetailView

# ----------------------------------------
from django.conf.urls import url, include
from . import views


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]
