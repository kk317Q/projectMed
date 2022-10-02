# Generated by Django 3.1.5 on 2021-04-04 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0013_auto_20210404_2253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='favouriteArticle',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='likedArticle',
        ),
        migrations.AddField(
            model_name='article',
            name='usersFaved',
            field=models.ManyToManyField(related_name='favouriteArticle', to='medapp.RegisteredUser'),
        ),
        migrations.AddField(
            model_name='article',
            name='usersLiked',
            field=models.ManyToManyField(related_name='likedArticle', to='medapp.RegisteredUser'),
        ),
    ]
