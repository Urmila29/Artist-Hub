# Generated by Django 2.0 on 2021-09-20 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AArtist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Profession', models.CharField(default='Profession', max_length=100)),
                ('Firstname', models.CharField(default='First name', max_length=100)),
                ('Lastname', models.CharField(default='Last name', max_length=100)),
                ('Email', models.EmailField(default='E-mail Address', max_length=100, unique=True)),
                ('Password', models.CharField(default='Password', max_length=100)),
                ('Repeatpassword', models.CharField(default='Repeat Password', max_length=100)),
                ('Nationality', models.CharField(default='Country Name', max_length=50)),
                ('Mobileno', models.BigIntegerField(default='123')),
                ('Birthdate', models.DateField(auto_now_add=True)),
                ('Currentaddr', models.CharField(default='Current Address', max_length=255)),
                ('Permanentaddr', models.CharField(default='Permanent Address', max_length=255)),
                ('Gender', models.CharField(default='Gender', max_length=10)),
                ('ProfilePic', models.ImageField(default='abc.png', upload_to='media/profile/')),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Admin.AAdmin')),
            ],
        ),
    ]