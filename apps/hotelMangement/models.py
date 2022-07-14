import os.path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
# Create your models here.
from django_lifecycle import LifecycleModelMixin, AFTER_CREATE, hook, AFTER_SAVE, AFTER_DELETE

import json, urllib


def getLatLon(address):
    address = urllib.parse.quote_plus(address)
    geo = urllib.request.urlopen("http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s" % (address))
    return geo.read()


class Hotel(LifecycleModelMixin, models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Phone number must be entered in the format +919999999999. equal to 10 digits "
                                         "allowed.")
    phone = models.CharField('Phone', validators=[phone_regex], max_length=10, unique=True, null=True)
    landline_number = models.CharField('Phone', validators=[phone_regex], max_length=10, unique=True, null=True)
    id = models.AutoField(primary_key=True)
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
    hotel_image_thumbnail = models.ImageField(upload_to='hotelImage_thumbs/', editable=False)
    hotel_logo_thumbnail = models.ImageField(upload_to='hotelLogo_thumbs/', editable=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        geo = json.loads(
            getLatLon("%s,%s,%s" % (self.address, self.city, self.zipcode)))
        if geo['status'] == "OK":
            self.latitude = geo['results'][0]['geometry']['location']['lat']
            self.longitude = geo['results'][0]['geometry']['location']['lng']

        if not self.make_thumbnail():
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(Hotel, self).save(*args, **kwargs)

    def make_thumbnail(self):

        image = Image.open(self.hotel_image)
        image1 = Image.open(self.hotel_logo)
        image.thumbnail((400, 400), Image.ANTIALIAS)
        image1.thumbnail((400, 400), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.hotel_image.name)
        thumb_extension = thumb_extension.lower()
        thumb_name1, thumb_extension1 = os.path.splitext(self.hotel_logo.name)
        thumb_extension1 = thumb_extension1.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        thumb_filename1 = thumb_name1 + '_thumb' + thumb_extension1

        if thumb_extension1 in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)
        # Save thumbnail to in-memory file as StringIO
        temp_thumb1 = BytesIO()
        image1.save(temp_thumb1, FTYPE)
        temp_thumb1.seek(0)
        # set save=False, otherwise it will run in an infinite loop
        self.hotel_image_thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        self.hotel_logo_thumbnail.save(thumb_filename1, ContentFile(temp_thumb1.read()), save=False)
        temp_thumb.close()
        temp_thumb1.close()

        return True

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
