# Generated by Django 5.1.1 on 2024-09-12 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0008_company_address_company_city_company_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='iataCassNumber',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='officeNumber',
            field=models.IntegerField(null=True),
        ),
    ]
