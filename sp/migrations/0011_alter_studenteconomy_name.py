# Generated by Django 4.0.5 on 2022-06-12 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0010_alter_studenteconomy_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studenteconomy',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sp.student'),
        ),
    ]
