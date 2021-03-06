# Generated by Django 4.0.5 on 2022-07-10 17:26

from django.db import migrations, models
import django.utils.timezone
import django_lifecycle.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('item_name', models.CharField(blank=True, max_length=100, null=True)),
                ('item_price', models.CharField(blank=True, max_length=100, null=True)),
                ('item_description', models.CharField(blank=True, max_length=100, null=True)),
                ('item_offer_price', models.CharField(blank=True, max_length=100, null=True)),
                ('item_image', models.ImageField(default='', null=True, upload_to='itemImage/')),
                ('item_thumbnail', models.ImageField(editable=False, upload_to='thumbs/')),
            ],
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
