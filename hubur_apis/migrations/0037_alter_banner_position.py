# Generated by Django 3.2.8 on 2023-03-28 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0036_auto_20230328_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='position',
            field=models.IntegerField(blank=True, choices=[(1, 'Top'), (2, 'Middle'), (3, 'After Have You Been There'), (4, 'Before My Favourites')], null=True),
        ),
    ]
