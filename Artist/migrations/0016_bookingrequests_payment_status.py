# Generated by Django 2.0 on 2021-10-23 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Artist', '0015_bookingrequests_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingrequests',
            name='Payment_Status',
            field=models.CharField(default='Pending', max_length=15),
        ),
    ]
