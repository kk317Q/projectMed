# Generated by Django 3.1.5 on 2021-04-05 23:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0022_auto_20210405_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respondcomment',
            name='datePosted',
            field=models.DateField(default=datetime.datetime(2021, 4, 5, 23, 14, 1, 950086)),
        ),
        migrations.AlterField(
            model_name='reviewarticle',
            name='datePosted',
            field=models.DateField(default=datetime.datetime(2021, 4, 5, 23, 14, 1, 949607)),
        ),
    ]
