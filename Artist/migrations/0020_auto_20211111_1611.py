# Generated by Django 2.0 on 2021-11-11 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Artist', '0019_auto_20211111_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='Rate',
            field=models.CharField(max_length=10),
        ),
    ]
