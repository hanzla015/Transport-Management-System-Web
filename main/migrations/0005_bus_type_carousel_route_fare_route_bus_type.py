# Generated by Django 4.1 on 2023-03-05 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_buse_driver'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head_line', models.CharField(default='', max_length=99)),
                ('desc_line', models.CharField(default='', max_length=99)),
                ('image_link', models.CharField(default='', max_length=999)),
            ],
        ),
        migrations.AddField(
            model_name='route',
            name='fare',
            field=models.IntegerField(default=400),
        ),
        migrations.AddField(
            model_name='route',
            name='bus_type',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='main.bus_type'),
        ),
    ]
