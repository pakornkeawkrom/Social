# Generated by Django 5.1.6 on 2025-03-03 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_delete_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='content',
            field=models.TextField(blank=True, default=''),
        ),
    ]
