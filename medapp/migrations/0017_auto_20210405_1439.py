# Generated by Django 3.1.5 on 2021-04-05 14:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0016_auto_20210405_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='respondcomment',
            name='body',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='respondcomment',
            name='datePosted',
            field=models.DateField(default=datetime.datetime(2021, 4, 5, 14, 39, 37, 640169)),
        ),
        migrations.AlterField(
            model_name='reviewarticle',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usersReviewOnArticle', to='medapp.registereduser'),
        ),
        migrations.AlterField(
            model_name='reviewarticle',
            name='datePosted',
            field=models.DateField(default=datetime.datetime(2021, 4, 5, 14, 39, 37, 639591)),
        ),
    ]
