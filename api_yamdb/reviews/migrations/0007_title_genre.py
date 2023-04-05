# Generated by Django 3.2 on 2023-04-02 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20230402_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='titles', through='reviews.GenreTitle', to='reviews.Genre', verbose_name='Жанр'),
        ),
    ]
