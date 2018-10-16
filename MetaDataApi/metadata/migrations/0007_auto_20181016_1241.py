# Generated by Django 2.1.2 on 2018-10-16 10:41

import MetaDataApi.metadata.custom_storages
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0006_auto_20181015_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schema',
            name='rdf_file',
            field=models.FileField(blank=True, null=True, storage=MetaDataApi.metadata.custom_storages.MediaStorage(), upload_to='schemas'),
        ),
    ]
