import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
# Create your models here.
from django_lifecycle import LifecycleModelMixin, AFTER_CREATE, hook, AFTER_SAVE, AFTER_DELETE


class Hotels(LifecycleModelMixin,models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Phone number must be entered in the format +919999999999. equal to 10 digits "
                                         "allowed.")
    phone = models.CharField('Phone', validators=[phone_regex], max_length=10, unique=True, null=True)
    landline_number = models.CharField('Phone', validators=[phone_regex], max_length=10, unique=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=250, unique=True)
    hotel_name = models.CharField(max_length=250, blank=True, null=True)
    manager_name = models.CharField(max_length=250, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    receive_newsletter = models.BooleanField(default=False)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    hotel_image = models.ImageField(null=True, upload_to='hotelImage/', default='')
    hotel_logo = models.ImageField(null=True, upload_to='hotelLogo/', default='')

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
        return str(self.hotel_name)
