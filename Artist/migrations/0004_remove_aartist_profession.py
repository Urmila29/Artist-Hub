# Generated by Django 2.0 on 2021-09-25 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Artist', '0003_auto_20210920_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aartist',
            name='Profession',
        ),
    ]