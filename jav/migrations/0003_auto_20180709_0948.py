# Generated by Django 2.0.7 on 2018-07-09 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jav', '0002_auto_20180709_0916'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='category',
            new_name='actress',
        ),
    ]
