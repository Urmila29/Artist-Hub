# Generated by Django 2.0 on 2021-09-25 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Artist', '0005_aartist_profession'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aartist',
            name='Profession',
        ),
    ]
