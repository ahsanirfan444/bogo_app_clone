# Generated by Django 3.2.8 on 2023-05-11 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0063_offers_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
