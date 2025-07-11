# Generated by Django 3.2.8 on 2023-04-27 11:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0053_contactus_country_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('persons', models.IntegerField(default=0)),
                ('date', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Accepted'), (3, 'Cancelled')])),
                ('reason', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('i_business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hubur_apis.business')),
                ('i_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Bookings',
            },
        ),
    ]
