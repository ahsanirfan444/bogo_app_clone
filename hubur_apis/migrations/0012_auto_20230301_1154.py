# Generated by Django 3.2.8 on 2023-03-01 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0011_alter_userprofile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='contact',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country_code',
            field=models.CharField(default='', max_length=5),
            preserve_default=False,
        ),
    ]
