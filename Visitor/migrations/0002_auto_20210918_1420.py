# Generated by Django 2.0 on 2021-09-18 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Visitor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vvisitor',
            name='Emailaddr',
        ),
        migrations.AddField(
            model_name='vvisitor',
            name='Email',
            field=models.EmailField(default='E-mail Address', max_length=100, unique=True),
        ),
    ]
