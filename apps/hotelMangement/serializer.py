from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from apps.hotelMangement.models import Hotel


class CreateHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'
