# Generated by Django 4.0.5 on 2022-06-12 00:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0006_rename_first_name_studenteconomy_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studenteconomy',
            name='economy',
        ),
    ]
