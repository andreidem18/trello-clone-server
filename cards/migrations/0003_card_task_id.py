# Generated by Django 2.2.24 on 2021-07-15 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20210710_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='task_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
