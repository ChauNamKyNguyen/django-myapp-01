# Generated by Django 2.0.7 on 2018-07-14 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jav', '0008_auto_20180713_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='actress',
            name='picture',
            field=models.ImageField(blank=True, upload_to='actress_images/'),
        ),
    ]