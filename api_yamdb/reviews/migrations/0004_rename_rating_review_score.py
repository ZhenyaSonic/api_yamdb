# Generated by Django 3.2 on 2024-01-31 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20240131_1925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='rating',
            new_name='score',
        ),
    ]