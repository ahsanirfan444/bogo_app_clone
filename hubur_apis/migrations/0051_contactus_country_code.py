# Generated by Django 3.2.8 on 2023-04-27 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0050_contactus'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='country_code',
            field=models.CharField(default='', max_length=5),
            preserve_default=False,
        ),
    ]
