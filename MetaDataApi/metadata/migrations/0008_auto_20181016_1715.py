# Generated by Django 2.1.2 on 2018-10-16 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0007_auto_20181016_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='objectrelation',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='object',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schema',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]