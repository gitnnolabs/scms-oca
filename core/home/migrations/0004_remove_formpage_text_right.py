# Generated by Django 3.2.12 on 2022-05-31 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_formfield_formpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formpage',
            name='text_right',
        ),
    ]
