# Generated by Django 2.1.1 on 2018-09-17 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('datatype', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('origin', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='object',
            name='schema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metadata.Schema'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metadata.Object'),
        ),
    ]
