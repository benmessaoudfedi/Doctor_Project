# Generated by Django 3.2.2 on 2021-05-28 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0002_auto_20210528_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='carte_cin',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
