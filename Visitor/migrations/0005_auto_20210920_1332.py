# Generated by Django 2.0 on 2021-09-20 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Visitor', '0004_auto_20210920_1235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vvisitor',
            name='Email',
        ),
        migrations.RemoveField(
            model_name='vvisitor',
            name='Password',
        ),
        migrations.RemoveField(
            model_name='vvisitor',
            name='Repeatpassword',
        ),
    ]
