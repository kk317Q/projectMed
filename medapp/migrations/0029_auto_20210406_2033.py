# Generated by Django 3.1.5 on 2021-04-06 20:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0028_auto_20210406_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='registereduser',
            name='malefemale',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='respondcomment',
            name='datePosted',
            field=models.DateField(default=datetime.datetime(2021, 4, 6, 20, 33, 36, 320507)),
        ),
        migrations.AlterField(
            model_name='reviewarticle',
            name='datePosted',
            field=models.DateField(default=datetime.datetime(2021, 4, 6, 20, 33, 36, 320036)),
        ),
    ]
