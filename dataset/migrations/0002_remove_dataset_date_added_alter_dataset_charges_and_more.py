# Generated by Django 5.1.3 on 2024-11-21 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='date_added',
        ),
        migrations.AlterField(
            model_name='dataset',
            name='charges',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='department',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]
