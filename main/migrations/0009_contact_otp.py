# Generated by Django 4.1 on 2023-03-05 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_routine_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('serial_no', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('phone', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(default='', max_length=100)),
                ('content', models.TextField()),
                ('time_stamp', models.TimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.IntegerField(blank=True)),
                ('time_stamp', models.DateTimeField(auto_now=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
