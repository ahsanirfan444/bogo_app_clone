# Generated by Django 3.2.8 on 2023-07-27 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0125_usersubscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hubur_apis.usersubscription'),
        ),
    ]
