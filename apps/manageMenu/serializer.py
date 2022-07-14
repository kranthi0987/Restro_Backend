from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from apps.manageMenu.models import Menu, SubMenu, Item


class CreateMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class CreateSubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenu
        fields = '__all__'


class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
