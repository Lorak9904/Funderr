# Generated by Django 5.1.1 on 2024-09-28 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0014_remove_priorytet_konkurs_remove_firma_konkursy_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='firma',
            name='tags',
            field=models.CharField(max_length=255, null=True, verbose_name='taki'),
        ),
        migrations.AddField(
            model_name='ngo',
            name='tags',
            field=models.CharField(max_length=255, null=True, verbose_name='taki'),
        ),
    ]
