# Generated by Django 3.1.5 on 2021-04-05 10:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0014_auto_20210404_2255'),
    ]

    operations = [
        migrations.CreateModel(
            name='respondComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorType', models.CharField(max_length=100)),
                ('datePosted', models.DateField(default=datetime.datetime(2021, 4, 5, 10, 25, 14, 371890))),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medapp.registereduser')),
            ],
        ),
        migrations.CreateModel(
            name='reviewArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorType', models.CharField(max_length=100)),
                ('datePosted', models.DateField(default=datetime.datetime(2021, 4, 5, 10, 25, 14, 371412))),
                ('body', models.CharField(max_length=1000)),
                ('stars', models.IntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medapp.registereduser')),
            ],
        ),
        migrations.RemoveField(
            model_name='docreview',
            name='review_ptr',
        ),
        migrations.RemoveField(
            model_name='likearticle',
            name='article',
        ),
        migrations.DeleteModel(
            name='ArtReview',
        ),
        migrations.DeleteModel(
            name='DocReview',
        ),
        migrations.DeleteModel(
            name='likeArticle',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.AddField(
            model_name='respondcomment',
            name='reviewArticle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medapp.reviewarticle'),
        ),
    ]