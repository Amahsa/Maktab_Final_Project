# from typing_extensions import Required
from django.db.models import fields
from rest_framework import serializers
from .models import *




class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Task
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    tasks =  serializers.StringRelatedField(many=True, read_only = True , required= False)
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Category
        fields = ['id','owner','category_name','description','tasks']

