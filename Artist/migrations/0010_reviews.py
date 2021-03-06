# Generated by Django 2.0 on 2021-10-06 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Artist', '0009_aartist_profession'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rate', models.IntegerField()),
                ('Visitor_name', models.CharField(default='Firstname Lastname', max_length=100)),
                ('Title', models.CharField(default='Title', max_length=100)),
                ('Review', models.TextField(max_length=5000)),
                ('Review_Created_Date', models.DateField(auto_now_add=True)),
                ('artistkey', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Artist.AArtist')),
            ],
        ),
    ]
