# Generated by Django 3.2.8 on 2023-04-18 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0043_voting'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='i_business',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hubur_apis.business'),
        ),
    ]
