# Generated by Django 3.2.8 on 2023-03-09 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0020_alter_userprofile_dob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinterest',
            name='i_subcategory',
        ),
        migrations.RemoveField(
            model_name='userinterest',
            name='is_active',
        ),
        migrations.AddField(
            model_name='userinterest',
            name='i_category',
            field=models.ManyToManyField(to='hubur_apis.Category'),
        ),
    ]
