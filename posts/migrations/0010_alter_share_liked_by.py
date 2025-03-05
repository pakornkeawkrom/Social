# Generated by Django 5.1.6 on 2025-03-03 15:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_remove_comment_share_post_share_count'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='liked_shares', to=settings.AUTH_USER_MODEL),
        ),
    ]
