# Generated by Django 3.2.12 on 2022-07-28 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disclosure_directory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='disclosuredirectory',
            name='end_date',
            field=models.DateField(blank=True, max_length=255, null=True, verbose_name='End Date'),
        ),
        migrations.AddField(
            model_name='disclosuredirectory',
            name='end_time',
            field=models.TimeField(blank=True, max_length=255, null=True, verbose_name='End Time'),
        ),
        migrations.AddField(
            model_name='disclosuredirectory',
            name='start_date',
            field=models.DateField(blank=True, max_length=255, null=True, verbose_name='Start Date'),
        ),
        migrations.AddField(
            model_name='disclosuredirectory',
            name='start_time',
            field=models.TimeField(blank=True, max_length=255, null=True, verbose_name='Start Time'),
        ),
    ]
