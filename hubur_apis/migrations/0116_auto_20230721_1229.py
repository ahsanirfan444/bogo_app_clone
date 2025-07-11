# Generated by Django 3.2.8 on 2023-07-21 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0115_content_description_ar'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='description_ar',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='level',
            name='name_ar',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='level',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, 'Gold'), (2, 'Silver'), (3, 'Bronze')], default=3),
        ),
    ]
