# Generated by Django 4.0.5 on 2022-07-10 16:37

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import django_lifecycle.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('phone', models.CharField(max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format +919999999999. equal to 10 digits allowed.', regex='^\\+?1?\\d{9,10}$')], verbose_name='Phone')),
                ('landline_number', models.CharField(max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format +919999999999. equal to 10 digits allowed.', regex='^\\+?1?\\d{9,10}$')], verbose_name='Phone')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('hotel_name', models.CharField(blank=True, max_length=250, null=True)),
                ('manager_name', models.CharField(blank=True, max_length=250, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('receive_newsletter', models.BooleanField(default=False)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=100, null=True)),
                ('hotel_image', models.ImageField(default='', null=True, upload_to='hotelImage/')),
                ('hotel_logo', models.ImageField(default='', null=True, upload_to='hotelLogo/')),
            ],
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]