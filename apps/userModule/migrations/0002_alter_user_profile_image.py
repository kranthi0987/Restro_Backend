# Generated by Django 4.0.5 on 2022-06-11 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userModule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(default='', null=True, upload_to='profile/'),
        ),
    ]
