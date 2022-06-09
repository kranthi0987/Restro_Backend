from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django_lifecycle import LifecycleModelMixin, hook, AFTER_SAVE, AFTER_DELETE, LifecycleModel, AFTER_CREATE

# Create your models here.

user_roles = (
    ('SuperAdmin', 'SuperAdmin'),
    ('FieldUser', 'FieldUser'),
    ('Manager', 'Manager')
)


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        user = self._create_user(username, email, password, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


class User(LifecycleModelMixin, AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Phone number must be entered in the format +919999999999. equal to 10 digits "
                                         "allowed.")
    phone = models.CharField('Phone', validators=[phone_regex], max_length=10, unique=True, null=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=250, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    receive_newsletter = models.BooleanField(default=False)
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True, default="FieldUser", choices=user_roles)
    about_me = models.TextField(max_length=500, blank=True, null=True)
    profile_image = models.ImageField(null=True, upload_to='profile/', default='')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['username', 'phone', 'email']

    objects = UserManager()

    @hook(AFTER_CREATE)
    def on_content_created(self):
        pass

    @hook(AFTER_SAVE)
    def on_content_saved(self):
        pass

    @hook(AFTER_DELETE)
    def on_content_deleted(self):
        pass

    def __str__(self):
        return str(self.username)


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Phone number must be entered in the format +919999999999. Up to 14 digits "
                                         "allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of otp_sent')
    validated = models.BooleanField(default=False,
                                    help_text='If it is true, that means user have validate otp correctly in second API')
    otp_session_id = models.CharField(max_length=120, null=True, default="")

    # username = models.CharField(max_length=20, blank=True, null=True, default=None)
    # email = models.CharField(max_length=50, null=True, blank=True, default=None)
    # password = models.CharField(max_length=100, null=True, blank=True, default=None)

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)
