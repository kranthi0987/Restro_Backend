from django.urls import re_path, path

from apps.userModule.views import *
from apps.userModule import views

urlpatterns = [
    re_path('^validate_register_phone', ValidatePhoneSendOTP.as_view()),
    re_path('^validate_register_otp', ValidateOTP.as_view()),
    re_path('^validate_login_phone', ValidatePhoneSendOTPLogin.as_view()),
    re_path('^validate_login_otp', ValidateOTPLogin.as_view()),
    path('register', Register.as_view()),
    # re_path('^login', LoginAPI.as_view()),
    re_path('^loginemail', LoginWithEmail.as_view()),
    path('registerwithemail', RegisterWithEmail.as_view()),
    path('getallusers', GetAllUsers.as_view()),
    path('activate/<pk>', views.user_activate),
    path('deactivate/<pk>', views.user_deactivate),
    path(r'emailactivate/<uidb64>/<token>/',emailactivate, name='emailactivate'),
]
