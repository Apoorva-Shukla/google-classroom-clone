# Generated by Django 3.1.7 on 2021-06-01 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_class', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='slug',
            field=models.SlugField(blank=True, max_length=40),
        ),
    ]
