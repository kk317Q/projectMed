# Generated by Django 3.1.5 on 2021-04-07 18:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0030_auto_20210407_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='datePosted',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 7, 18, 16, 48, 124078)),
        ),
        migrations.AlterField(
            model_name='respondcomment',
            name='datePosted',
            field=models.DateField(default=datetime.datetime(2021, 4, 7, 18, 16, 48, 131036)),
        ),
        migrations.AlterField(
            model_name='reviewarticle',
            name='datePosted',
            field=models.DateField(default=datetime.datetime(2021, 4, 7, 18, 16, 48, 130489)),
        ),
    ]
