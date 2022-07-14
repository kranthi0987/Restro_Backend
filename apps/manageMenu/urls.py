from django.template.defaulttags import url
from django.urls import re_path, path

from apps.manageMenu import views
from apps.manageMenu.views import *

urlpatterns = [
    path('menu/list/', views.menu_list),
    path('menu/create/', views.create_menu),
    path('menu/listbyid/', views.menu_list_byid),
    path('menu/<int:pk>', views.menu_detail),

    path('submenu/list/', views.submenu_list),
    path('submenu/create/', views.create_submenu),
    path('submenu/listbyid/', views.submenu_list_byid),
    path('submenu/<int:pk>', views.submenu_detail),

    path('item/list/', views.item_list),
    path('item/create/', views.create_item),
    path('item/listbyid/', views.item_list_byid),
    path('item/<int:pk>', views.item_detail),
]
