# Generated by Django 3.1.6 on 2021-03-01 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_auto_20210226_0748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweets',
            name='created_utc',
        ),
        migrations.AddField(
            model_name='tweets',
            name='create_time',
            field=models.DateTimeField(null=True),
        ),
    ]
