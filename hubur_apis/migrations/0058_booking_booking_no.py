# Generated by Django 3.2.8 on 2023-04-28 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0057_auto_20230428_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_no',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
