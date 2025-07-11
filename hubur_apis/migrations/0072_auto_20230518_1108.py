# Generated by Django 3.2.8 on 2023-05-18 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hubur_apis', '0071_auto_20230512_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='platform',
            field=models.IntegerField(choices=[(1, 'Mobile'), (2, 'Web')], default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='banner',
            name='position',
            field=models.IntegerField(choices=[(1, 'Top'), (2, 'Middle'), (3, 'After Have You Been There'), (4, 'Before My Favourites'), (5, 'Catagory Page')]),
        ),
        migrations.RemoveField(
            model_name='content',
            name='i_sub_category',
        ),
        migrations.AddField(
            model_name='content',
            name='i_sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hubur_apis.subcategories'),
        ),
    ]
