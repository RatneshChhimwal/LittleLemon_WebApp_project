# Generated by Django 4.1.3 on 2024-08-08 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_menu_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='description',
            new_name='menu_item_description',
        ),
    ]
