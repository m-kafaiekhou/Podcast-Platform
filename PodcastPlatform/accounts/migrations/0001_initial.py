# Generated by Django 4.2.5 on 2023-09-14 15:54

import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('phone_number', models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(message='Invalid Phone number. Phone number must be like: +989XXXXXXXXX or 09XXXXXXXXX', regex='^(\\+989|09)+\\d{9}$')], verbose_name='Phone Number')),
                ('first_name', models.CharField(max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activation Status')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff Status')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Superuser Status')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
    ]