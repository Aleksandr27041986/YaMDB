# Generated by Django 3.2 on 2023-03-29 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, db_table='genre_title', related_name='titles', to='reviews.Genre'),
        ),
    ]