# Generated by Django 4.0.5 on 2022-07-08 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userModule', '0002_alter_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('SuperAdmin', 'SuperAdmin'), ('FieldUser', 'FieldUser'), ('Manager', 'Manager')], default='FieldUser', max_length=100, null=True),
        ),
    ]
