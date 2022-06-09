from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from apps.manageMenu.models import Menu


class CreateMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
