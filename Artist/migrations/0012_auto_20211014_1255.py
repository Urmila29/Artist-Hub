# Generated by Django 2.0 on 2021-10-14 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Artist', '0011_auto_20211006_1551'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookingrequests',
            old_name='artistkey',
            new_name='artist',
        ),
        migrations.RenameField(
            model_name='bookingrequests',
            old_name='visitorkey',
            new_name='visitor',
        ),
        migrations.RenameField(
            model_name='reviews',
            old_name='artistkey',
            new_name='artist',
        ),
        migrations.RenameField(
            model_name='reviews',
            old_name='visitorkey',
            new_name='visitor',
        ),
    ]
