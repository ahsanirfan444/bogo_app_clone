# Generated by Django 3.2.8 on 2023-02-27 05:56

from django.db import migrations, models
import django.db.models.deletion
import global_methods


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0004_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaimBusiness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('business_email', models.EmailField(max_length=50, unique=True)),
                ('trade_license_number', models.CharField(max_length=50)),
                ('trade_license', models.FileField(upload_to='trade_license/', validators=[global_methods.file_size])),
                ('approve', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('i_business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hubur_apis.business')),
            ],
            options={
                'verbose_name_plural': 'Claim Business',
                'db_table': 'claim_business_db',
                'ordering': ['-created_at'],
            },
        ),
    ]
