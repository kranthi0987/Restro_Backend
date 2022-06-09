# Generated by Django 4.0.5 on 2022-07-10 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelMangement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='hotel_image_thumbnail',
            field=models.ImageField(default=11, editable=False, upload_to='hotelImage_thumbs/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_logo_thumbnail',
            field=models.ImageField(default=11, editable=False, upload_to='hotelLogo_thumbs/'),
            preserve_default=False,
        ),
    ]