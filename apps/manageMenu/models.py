from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
# Create your models here.
from django_lifecycle import LifecycleModelMixin, AFTER_CREATE, hook, AFTER_SAVE, AFTER_DELETE
import os.path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

from apps.hotelMangement.models import Hotel

category = (
    ('MainCategory', 'MainCategory'),
    ('SubCategory', 'SubCategory'),
)


class Menu(LifecycleModelMixin, models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    hotel_id = models.ForeignKey(Hotel, null=True, on_delete=models.SET_NULL)
    menu_name = models.CharField(max_length=100, blank=True, null=True)
    menu_description = models.CharField(max_length=100, blank=True, null=True)

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
        return str(self.menu_name)


class SubMenu(LifecycleModelMixin, models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    menu_id = models.ForeignKey(Menu, null=True, on_delete=models.SET_NULL)
    submenu_name = models.CharField(max_length=100, blank=True, null=True)
    submenu_description = models.CharField(max_length=100, blank=True, null=True)

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
        return str(self.submenu_name)


class Item(LifecycleModelMixin, models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=100, blank=True, null=True, default="SubCategory", choices=category)
    sub_menu_id = models.ForeignKey(SubMenu, null=True, on_delete=models.SET_NULL)
    item_name = models.CharField(max_length=100, blank=True, null=True)
    item_price = models.CharField(max_length=100, blank=True, null=True)
    item_description = models.CharField(max_length=100, blank=True, null=True)
    item_offer_price = models.CharField(max_length=100, blank=True, null=True)
    item_image = models.ImageField(null=True, upload_to='itemImage/', default='')
    item_thumbnail = models.ImageField(upload_to='items_thumbs/', editable=False)
    is_veg = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if not self.make_thumbnail():
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(Item, self).save(*args, **kwargs)

    def make_thumbnail(self):

        image = Image.open(self.item_image)
        image.thumbnail((400, 400), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.item_image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
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

        # set save=False, otherwise it will run in an infinite loop
        self.item_thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

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
        return str(self.item_name)
