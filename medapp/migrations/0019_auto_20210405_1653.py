# Generated by Django 3.1.5 on 2021-04-05 16:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0018_auto_20210405_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='artIMG',
        ),
        migrations.AddField(
            model_name='article',
            name='articleIMG',
            field=models.ImageField(default='articleIMG/default.jpg', null=True, upload_to='articleIMG/'),
        ),
        migrations.AlterField(
            model_name='respondcomment',
            name='datePosted',
            field=models.DateField(default=datetime.datetime(2021, 4, 5, 16, 53, 5, 294431)),
        ),
        migrations.AlterField(
            model_name='reviewarticle',
            name='datePosted',
            field=models.DateField(default=datetime.datetime(2021, 4, 5, 16, 53, 5, 293883)),
        ),
    ]