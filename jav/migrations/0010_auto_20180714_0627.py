# Generated by Django 2.0.7 on 2018-07-14 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jav', '0009_actress_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actress',
            old_name='picture',
            new_name='image',
        ),
    ]
