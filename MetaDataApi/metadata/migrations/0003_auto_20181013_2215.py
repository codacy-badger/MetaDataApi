# Generated by Django 2.1.2 on 2018-10-13 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0002_auto_20181012_2034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objectrelation',
            name='url',
        ),
        migrations.AddField(
            model_name='objectrelation',
            name='schema',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='object_relations', to='metadata.Schema'),
            preserve_default=False,
        ),
    ]