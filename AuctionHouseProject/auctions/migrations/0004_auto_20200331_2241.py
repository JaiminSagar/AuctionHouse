# Generated by Django 3.0.4 on 2020-03-31 17:11

import auctions.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200331_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyfilesupload',
            name='document',
            field=models.FileField(blank=True, upload_to=auctions.models.generate_filename),
        ),
    ]