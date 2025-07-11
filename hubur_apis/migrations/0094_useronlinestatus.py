# Generated by Django 3.2.8 on 2023-06-14 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0093_chat_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOnlineStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_online', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('i_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Online Status',
                'db_table': 'user_online_status_db',
                'ordering': ['-created_at'],
            },
        ),
    ]
