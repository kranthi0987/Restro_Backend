from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

User = get_user_model()


class EmailUserDataSerializer(serializers.Serializer):
    string_field = serializers.CharField(required=True)
    number_field = serializers.IntegerField(required=True)
    float_field = serializers.FloatField(required=True)
    url_field = serializers.URLField(required=True)
    email_field = serializers.EmailField(required=True)
    date_field = serializers.DateField(required=True)
    time_field = serializers.TimeField(required=True)


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = (
            'username', 'email', 'phone', 'password', 'first_name', 'last_name', 'receive_newsletter', 'date_of_birth',
            'address', 'city', 'about_me', 'profile_image', 'country', 'state', 'zipcode', 'role')
        extra_kwargs = {'password': {'write_only': True}, }

        def create(self, validated_data):
            user = User.objects.create(**validated_data)
            return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'phone', 'first_name', 'last_name', 'last_login', 'receive_newsletter',
            'date_of_birth',
            'address', 'city', 'about_me', 'profile_image', 'country', 'state', 'zipcode', 'role', 'is_active')


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False
    )

    def validate(self, data):
        print(data)
        phone = data.get('phone')
        password = data.get('password')

        if phone and password:
            if User.objects.filter(phone=phone).exists():
                print(phone, password)
                username = User.objects.get(phone=phone)
                # user = authenticate(request=self.context.get('request'), phone=phone, password=password)
                user = authenticate(request=self.context.get('request'), username=username.username, password=password)
                # print(user.phone)

            else:
                msg = {
                    'detail': 'phone number not found',
                    'status': False,
                }
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Username and password not matching. Try again',
                    'status': False,
                }
                raise serializers.ValidationError(msg, code='authorization')


        else:
            msg = {
                'detail': 'Phone number and password not found in request',
                'status': False,
            }
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data


class LoginEmailSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        print(data)
        email = data.get('email')
        password = data.get('password')

        if email and password:
            if User.objects.filter(email=email).exists():
                print(email, password)
                username = User.objects.get(email=email)
                # user = authenticate(request=self.context.get('request'), phone=phone, password=password)
                user = authenticate(request=self.context.get('request'), username=username.username, password=password)
                # print(user.phone)
                print(user)

            else:
                msg = {
                    'detail': 'Username number not found',
                    'status': False,
                }
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Username and password not matching. Try again',
                    'status': False,
                }
                raise serializers.ValidationError(msg, code='authorization')


        else:
            msg = {
                'detail': 'Phone number and password not found in request',
                'status': False,
            }
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data
