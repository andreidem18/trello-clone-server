# Generated by Django 2.2.24 on 2021-07-10 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='img_url',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
    ]
