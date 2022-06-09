from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from apps.hotelMangement.models import Hotels


class CreateHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotels
        fields = '__all__'
