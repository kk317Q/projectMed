# Generated by Django 3.1.5 on 2021-04-03 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medapp', '0005_auto_20210403_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultancy',
            name='closeStatusDoctor',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='consultancy',
            name='closeStatusPatient',
            field=models.BooleanField(default=True),
        ),
    ]