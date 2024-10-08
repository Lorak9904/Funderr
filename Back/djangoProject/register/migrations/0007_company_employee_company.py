# Generated by Django 5.1.1 on 2024-09-12 21:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0006_remove_employee_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='register.company'),
        ),
    ]
