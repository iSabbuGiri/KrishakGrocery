# Generated by Django 3.2.3 on 2021-07-06 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='latitute',
            field=models.FloatField(default=27.7090319),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='longitude',
            field=models.FloatField(default=85.2911131),
            preserve_default=False,
        ),
    ]
