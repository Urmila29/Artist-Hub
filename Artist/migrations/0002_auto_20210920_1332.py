# Generated by Django 2.0 on 2021-09-20 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Artist', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aartist',
            name='Email',
        ),
        migrations.RemoveField(
            model_name='aartist',
            name='Password',
        ),
        migrations.RemoveField(
            model_name='aartist',
            name='Repeatpassword',
        ),
    ]
