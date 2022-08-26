# Generated by Django 3.2.12 on 2022-08-26 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0004_institution_acronym'),
        ('event_directory', '0012_auto_20220825_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventdirectory',
            name='institutions',
        ),
        migrations.RemoveField(
            model_name='eventdirectory',
            name='organization',
        ),
        migrations.AddField(
            model_name='eventdirectory',
            name='organization',
            field=models.ManyToManyField(blank=True, help_text='Instituições responsáveis pela organização do evento.', to='institution.Institution', verbose_name='Instituição'),
        ),
    ]
