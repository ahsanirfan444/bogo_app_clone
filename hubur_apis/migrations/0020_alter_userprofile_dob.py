# Generated by Django 3.2.8 on 2023-03-09 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0019_alter_userprofile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
