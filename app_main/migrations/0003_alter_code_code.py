# Generated by Django 4.2.1 on 2023-06-29 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='code',
            field=models.TextField(verbose_name='Código'),
        ),
    ]
