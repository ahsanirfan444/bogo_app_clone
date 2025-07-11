# Generated by Django 3.2.8 on 2023-05-11 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0061_offers'),
    ]

    operations = [
        migrations.AddField(
            model_name='offers',
            name='i_content',
            field=models.ManyToManyField(to='hubur_apis.Content'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='position',
            field=models.IntegerField(choices=[(1, 'Top'), (2, 'Middle'), (3, 'After Have You Been There'), (4, 'Before My Favourites'), (5, 'Website'), (6, 'Catagory')]),
        ),
        migrations.RemoveField(
            model_name='offers',
            name='i_business',
        ),
        migrations.AddField(
            model_name='offers',
            name='i_business',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='hubur_apis.business'),
            preserve_default=False,
        ),
    ]
