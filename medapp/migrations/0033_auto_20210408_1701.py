# Generated by Django 3.1.5 on 2021-04-08 17:01

import datetime
from django.db import migrations, models
import medapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0032_auto_20210407_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='datePosted',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 8, 17, 1, 43, 288287)),
        ),
        migrations.AlterField(
            model_name='registereduser',
            name='profileIMG',
            field=models.ImageField(default='patientIcon.png', null=True, upload_to=medapp.models.profileImageDirectory),
        ),
        migrations.AlterField(
            model_name='respondcomment',
            name='datePosted',
            field=models.DateField(default=datetime.datetime(2021, 4, 8, 17, 1, 43, 295087)),
        ),
        migrations.AlterField(
            model_name='reviewarticle',
            name='datePosted',
            field=models.DateField(default=datetime.datetime(2021, 4, 8, 17, 1, 43, 294622)),
        ),
    ]
