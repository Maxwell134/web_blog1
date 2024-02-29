# Generated by Django 3.2 on 2024-02-25 09:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web_blog2', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='author',
        ),
        migrations.AlterField(
            model_name='post',
            name='date_published',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 25, 9, 53, 15, 707748, tzinfo=utc)),
        ),
    ]
