from django.template.defaulttags import url
from django.urls import re_path, path

from apps.hotelMangement import views
from apps.hotelMangement.views import *

urlpatterns = [
    path('hotel/list/', views.hotel_list),
    path('hotel/create/', views.create_hotel),
    path('hotel/listbyid/', views.hotel_list_byid),
    # url(r'^hotel/(?P<pk>[0-9]+)$', views.hotel_detail),
]
