# Generated by Django 4.0.5 on 2022-07-14 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelMangement', '0002_hotel_hotel_image_thumbnail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]