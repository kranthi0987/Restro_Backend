import http.client
import ast
import random
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .models import User, PhoneOTP
from .serializer import CreateUserSerializer, LoginSerializer, UserSerializer, LoginEmailSerializer
import environ

# Create your views here.
from .token import account_activation_token

env = environ.Env()
# reading .env file
environ.Env.read_env()
conn = http.client.HTTPConnection("2factor.in")


class ValidatePhoneSendOTP(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')

        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({
                    'code': 407,
                    'status': False,
                    'detail': 'Phone number already exists'
                })
            else:
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 10:
                            return Response({
                                'code': 403,
                                'status': False,
                                'detail': 'Sending otp error. Limit Exceeded. Please Contact Customer support'
                            })

                        old.count = count + 1
                        old.save()
                        print('Count Increase', count)

                        conn.request("GET",
                                     "https://2factor.in/API/R1/?module=SMS_OTP&apikey=" + env(
                                         '2FACTOR_API_KEY') + "&to=" + phone + "&otpvalue=" + str(
                                         key) + "&templatename=ArpinaOTP")
                        res = conn.getresponse()
                        data = res.read()
                        data = data.decode("utf-8")
                        data = ast.literal_eval(data)
                        if data["Status"] == 'Success':
                            old.otp_session_id = data["Details"]
                            old.save()
                            print('In validate phone :' + old.otp_session_id)
                            return Response({
                                'code': 201,
                                'status': True,
                                'detail': 'OTP sent successfully'
                            })
                        else:
                            return Response({
                                'code': 405,
                                'status': False,
                                'detail': 'OTP sending Failed'
                            })
                    else:
                        obj = PhoneOTP.objects.create(
                            phone=phone,
                            otp=key,
                            # email=email,
                            # username=username,
                            # password=password,
                        )
                        conn.request("GET",
                                     "https://2factor.in/API/R1/?module=SMS_OTP&apikey=" + env(
                                         '2FACTOR_API_KEY') + "&to=" + phone + "&otpvalue=" + str(
                                         key) + "&templatename=ArpinaOTP")
                        res = conn.getresponse()
                        data = res.read()
                        print(data.decode("utf-8"))
                        data = data.decode("utf-8")
                        data = ast.literal_eval(data)

                        if data["Status"] == 'Success':
                            obj.otp_session_id = data["Details"]
                            obj.save()
                            print('In validate phone :' + obj.otp_session_id)
                            return Response({
                                'code': 201,
                                'status': True,
                                'detail': 'OTP sent successfully'
                            })
                        else:
                            return Response({
                                'code': 405,
                                'status': False,
                                'detail': 'OTP sending Failed'
                            })
                else:
                    return Response({
                        'code': 406,
                        'status': False,
                        'detail': 'Sending otp error'
                    })
        else:
            return Response({
                'code': 205,
                'status': False,
                'detail': 'Phone number is not given in post request'
            })


class ValidateOTP(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                otp_session_id = old.otp_session_id
                print("In validate otp" + otp_session_id)
                conn.request("GET", "https://2factor.in/API/V1/" + env(
                    '2FACTOR_API_KEY') + "/SMS/VERIFY/" + otp_session_id + "/" + otp_sent)
                res = conn.getresponse()
                data = res.read()
                print(data.decode("utf-8"))
                data = data.decode("utf-8")
                data = ast.literal_eval(data)

                if data["Status"] == 'Success':
                    old.validated = True
                    old.save()
                    return Response({
                        'code': 206,
                        'status': True,
                        'detail': 'OTP MATCHED. Please proceed for registration.'
                    })

                else:
                    return Response({
                        'code': 408,
                        'status': False,
                        'detail': 'OTP INCORRECT'
                    })
            else:
                return Response({
                    'code': 409,
                    'status': False,
                    'detail': 'First Proceed via sending otp request'
                })
        else:
            return Response({
                'code': 410,
                'status': False,
                'detail': 'Please provide both phone and otp for Validation'
            })


class Register(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        username = request.data.get('username', False)
        email = request.data.get('email', False)

        if phone and username and email:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                validated = old.validated

                if validated:
                    serializer = CreateUserSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()
                    user.set_password('admin')
                    user.save()
                    old.delete()
                    return Response({
                        'code': 203,
                        'status': True,
                        'detail': 'Account Created Successfully'
                    })
                else:
                    return Response({
                        'code': 411,
                        'status': False,
                        'detail': 'OTP havent Verified. First do that Step.'
                    })
            else:
                return Response({
                    'code': 412,
                    'status': False,
                    'detail': 'Please verify Phone First'
                })
        else:
            return Response({
                'code': 413,
                'status': False,
                'detail': 'Both username, email, phone, password are not sent'
            })


# Register with email and password
class RegisterWithEmail(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        username = request.data.get('username', False)
        email = request.data.get('email', False)

        if phone and username and email:
            serializer = CreateUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user.set_password(request.data.get('password', False))
            user.is_active = False

            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('email/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )

            email.send()
            user.save()
            return Response({
                'code': 203,
                'status': True,
                'detail': 'Account Created Successfully',
                'message': 'email send'
            })
        else:
            return Response({
                'code': 413,
                'status': False,
                'detail': 'Both username, email, phone, password are not sent'
            })


# otp login with enter only phone number
class ValidatePhoneSendOTPLogin(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if not user.exists():
                return Response({
                    'code': 222,
                    'status': False,
                    'detail': 'Need to Register'
                })
            else:
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 10:
                            return Response({
                                'code': 403,
                                'status': False,
                                'detail': 'Sending otp error. Limit Exceeded. Please Contact Customer support'
                            })
                        old.count = count + 1
                        old.save()
                        print('Count Increase', count)

                        conn.request("GET",
                                     "https://2factor.in/API/R1/?module=SMS_OTP&apikey=" + env(
                                         '2FACTOR_API_KEY') + "&to=" + phone + "&otpvalue=" + str(
                                         key) + "&templatename=ArpinaOTP")
                        res = conn.getresponse()
                        data = res.read()
                        data = data.decode("utf-8")
                        data = ast.literal_eval(data)
                        if data["Status"] == 'Success':
                            old.otp_session_id = data["Details"]
                            old.save()
                            print('In validate phone :' + old.otp_session_id)
                            return Response({
                                'code': 201,
                                'status': True,
                                'detail': 'OTP sent successfully'
                            })
                        else:
                            return Response({
                                'code': 405,
                                'status': False,
                                'detail': 'OTP sending Failed'
                            })
                    else:
                        obj = PhoneOTP.objects.create(
                            phone=phone,
                            otp=key,
                        )
                        conn.request("GET",
                                     "https://2factor.in/API/R1/?module=SMS_OTP&apikey=" + env(
                                         '2FACTOR_API_KEY') + "&to=" + phone + "&otpvalue=" + str(
                                         key) + "&templatename=ArpinaOTP")
                        res = conn.getresponse()
                        data = res.read()
                        print(data.decode("utf-8"))
                        data = data.decode("utf-8")
                        data = ast.literal_eval(data)

                        if data["Status"] == 'Success':
                            obj.otp_session_id = data["Details"]
                            obj.save()
                            print('In validate phone :' + obj.otp_session_id)
                            return Response({
                                'code': 201,
                                'status': True,
                                'detail': 'OTP sent successfully'
                            })
                        else:
                            return Response({
                                'code': 405,
                                'status': False,
                                'detail': 'OTP sending Failed'
                            })
                else:
                    return Response({
                        'code': 406,
                        'status': False,
                        'detail': 'Sending otp error'
                    })
        else:
            return Response({
                'code': 205,
                'status': False,
                'detail': 'Phone number is not given in post request'
            }, status=400)


# login with otp need to enter otp,phone number
class ValidateOTPLogin(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                otp_session_id = old.otp_session_id
                print("In validate otp" + otp_session_id)
                conn.request("GET", "https://2factor.in/API/V1/" + env(
                    '2FACTOR_API_KEY') + "/SMS/VERIFY/" + otp_session_id + "/" + otp_sent)
                res = conn.getresponse()
                data = res.read()
                data = data.decode("utf-8")
                data = ast.literal_eval(data)

                if data["Status"] == 'Success':
                    old.validated = True
                    old.save()
                    temp_data = {
                        # 'username': old.username,
                        # 'email': old.email,
                        'phone': phone,
                        'password': 'admin'

                    }
                    serializer = LoginSerializer(data=temp_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.validated_data['user']
                    old.delete()
                    # login(request, user)
                    # return super().post(request, format=None)
                    return Response({
                        'code': 200,
                        'status': True,
                        "user": UserSerializer(user).data,
                        "token": AuthToken.objects.create(user)[1]
                    })
                    # return Response({
                    #     'status': True,
                    #     'detail': 'OTP MATCHED. Please proceed for registration.'
                    # })

                else:
                    return Response({
                        'code': 408,
                        'status': False,
                        'detail': 'OTP INCORRECT'
                    })
            else:
                return Response({
                    'code': 409,
                    'status': False,
                    'detail': 'First Proceed via sending otp request'
                })
        else:
            return Response({
                'code': 410,
                'status': False,
                'detail': 'Please provide both phone and otp for Validation'
            })


class LoginWithEmail(generics.GenericAPIView):
    serializer_class = LoginEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        return Response({
            'code': 200,
            'status': True,
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })


# get all users
class GetAllUsers(APIView):
    # @api_view(["GET"])
    try:
        @permission_classes([IsAuthenticated])
        @method_decorator(cache_page(60 * 1))
        @method_decorator(vary_on_cookie)
        def get(self, request):
            if request.user.is_authenticated:
                if request.user.role == 'SuperAdmin':
                    users = User.objects.all()
                else:
                    users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                return Response({'users': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response('user is not authenticated', status=status.HTTP_200_OK)
    except Exception as e:
        print("exception", e)
        raise e


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def user_activate(request, *args, **kwargs):
    """
    activate user
    """
    if request.method == 'POST':
        if request.user.role == 'SuperAdmin':
            userid = kwargs.get('pk')
            try:
                user = User.objects.filter(pk=userid).update(is_active=True)
                if user is None:
                    return Response("user not updated", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("user  updated", status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response("user not found", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You dont have enough permission to edit user",
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def user_deactivate(request, *args, **kwargs):
    """
        deactivate user
        """
    if request.method == 'POST':
        if request.user.role == 'SuperAdmin':
            userid = kwargs.get('pk')
            try:
                user = User.objects.filter(pk=userid).update(is_active=False)
                if user is None:
                    return Response("user not updated", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("user  updated", status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response("user not found", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You dont have enough permission to edit user",
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# Login Old Method
# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request, format=None):
#         phone = request.data.get('phone', False)
#         password = request.data.get('password', 'admin')
#
#         if phone and password:
#             old = PhoneOTP.objects.filter(phone__iexact=phone)
#             if old.exists():
#                 old = old.first()
#                 validated = old.validated
#
#                 if validated:
#                     temp_data = {
#                         # 'username': old.username,
#                         # 'email': old.email,
#                         'phone': phone,
#                         'password': password,
#
#                     }
#                     # serializer = CreateUserSerializer(data=request.data)
#                     # serializer.is_valid(raise_exception=True)
#                     # user = serializer.save()
#                     # user.set_password(password)
#                     # user.save()
#                     # print(user)
#                     # print(password)
#                     old.delete()
#                     serializer = LoginSerializer(data=temp_data)
#                     serializer.is_valid(raise_exception=True)
#                     user = serializer.validated_data['user']
#                     old.delete()
#                     # login(request, user)
#                     # return super().post(request, format=None)
#                     return Response({
#                         'status': True,
#                         "user": UserSerializer(user).data,
#                         "token": AuthToken.objects.create(user)[1]
#                     })
#                 else:
#                     return Response({
#                         'status': False,
#                         'detail': 'OTP havent Verified. First do that Step.'
#                     })
#             else:
#                 return Response({
#                     'status': False,
#                     'detail': 'Please verify Phone First'
#                 })
#         else:
#             return Response({
#                 'status': False,
#                 'detail': 'Both username, email, phone, password are not sent'
#             })


def send_otp(phone):
    if phone:
        key = random.randint(0000, 9999)
        print(key)
        return key
    else:
        return False


def emailactivate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse({'msg':'Thank you for your email confirmation. Now you can login your account.'})
    else:
        return HttpResponse({'msg':'Activation link is invalid!'})
