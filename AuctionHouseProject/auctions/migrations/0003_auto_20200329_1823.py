# Generated by Django 3.0.4 on 2020-03-29 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200329_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyreg',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
