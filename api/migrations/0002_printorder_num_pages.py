# Generated by Django 5.1.6 on 2025-03-07 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='printorder',
            name='num_pages',
            field=models.IntegerField(default=1),
        ),
    ]
