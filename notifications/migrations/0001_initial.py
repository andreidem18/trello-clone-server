# Generated by Django 2.2.24 on 2021-07-10 17:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('text', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity', to='boards.Board')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
