# Generated by Django 2.0.7 on 2018-07-13 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jav', '0007_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, upload_to='profile_images/'),
        ),
    ]
