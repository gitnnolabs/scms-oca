# Generated by Django 3.2.12 on 2023-02-15 18:43

from django.db import migrations, models
import django.db.models.deletion
import education_directory.models


class Migration(migrations.Migration):
    dependencies = [
        ("usefulmodels", "0011_auto_20221108_2356"),
        ("education_directory", "0002_alter_educationdirectory_record_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="educationdirectory",
            name="action",
            field=models.ForeignKey(
                blank=True,
                default=education_directory.models.get_default_action,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="usefulmodels.action",
                verbose_name="Ação",
            ),
        ),
    ]
