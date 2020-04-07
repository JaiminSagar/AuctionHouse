# Generated by Django 3.0.4 on 2020-04-05 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200403_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='currentauction',
            name='image_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='auctions.PropertyImagesUpload'),
        ),
        migrations.AlterField(
            model_name='currentauction',
            name='current_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='currentauction',
            name='increment_ratio',
            field=models.FloatField(default=0.05),
        ),
    ]
