# Generated by Django 2.2.24 on 2021-07-10 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20210710_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='img_url',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
    ]