# Generated by Django 3.2.8 on 2023-02-28 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0007_userprofile_terms_conditions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(max_length=30),
        ),
    ]
