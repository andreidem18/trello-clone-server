# Generated by Django 2.2.24 on 2021-07-12 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_auto_20210712_1547'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='template_url',
            new_name='img_url',
        ),
    ]