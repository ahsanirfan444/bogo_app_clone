# Generated by Django 3.2.8 on 2023-06-01 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0088_rewardpoints_userreward'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='type',
            field=models.IntegerField(choices=[(1, 'Daily'), (2, 'Weekly'), (3, 'Monthly'), (4, 'Hot')], default=1),
        ),
    ]
