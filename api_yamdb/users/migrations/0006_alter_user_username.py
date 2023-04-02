# Generated by Django 3.2 on 2023-03-31 11:16

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, help_text='Обязательное поле, только цифры, буквы или @/./+/-/_.', max_length=150, null=True, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Никнеим'),
        ),
    ]