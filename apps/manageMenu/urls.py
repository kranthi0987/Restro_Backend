from django.template.defaulttags import url
from django.urls import re_path, path

from apps.manageMenu import views
from apps.manageMenu.views import *

urlpatterns = [
    path('menu/list/', views.hotel_list),
    path('menu/create/', views.create_hotel),
    path('menu/listbyid/', views.hotel_list_byid),
    path('menu/<int:pk>', views.hotel_detail),
]
