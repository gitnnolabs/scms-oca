# Generated by Django 3.2.12 on 2022-10-28 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usefulmodels', '0008_auto_20221027_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='capital',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Capital of the Country'),
        ),
    ]
