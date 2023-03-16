# Generated by Django 1.9.5 on 2016-08-04 02:13
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CrontabSchedule",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "minute",
                    models.CharField(default="*", max_length=64, verbose_name="minute"),
                ),
                (
                    "hour",
                    models.CharField(default="*", max_length=64, verbose_name="hour"),
                ),
                (
                    "day_of_week",
                    models.CharField(
                        default="*", max_length=64, verbose_name="day of week"
                    ),
                ),
                (
                    "day_of_month",
                    models.CharField(
                        default="*", max_length=64, verbose_name="day of month"
                    ),
                ),
                (
                    "month_of_year",
                    models.CharField(
                        default="*", max_length=64, verbose_name="month of year"
                    ),
                ),
            ],
            options={
                "ordering": [
                    "month_of_year",
                    "day_of_month",
                    "day_of_week",
                    "hour",
                    "minute",
                ],
                "verbose_name": "crontab",
                "verbose_name_plural": "crontabs",
            },
        ),
        migrations.CreateModel(
            name="IntervalSchedule",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("every", models.IntegerField(verbose_name="every")),
                (
                    "period",
                    models.CharField(
                        choices=[
                            ("days", "Days"),
                            ("hours", "Hours"),
                            ("minutes", "Minutes"),
                            ("seconds", "Seconds"),
                            ("microseconds", "Microseconds"),
                        ],
                        max_length=24,
                        verbose_name="period",
                    ),
                ),
            ],
            options={
                "ordering": ["period", "every"],
                "verbose_name": "interval",
                "verbose_name_plural": "intervals",
            },
        ),
        migrations.CreateModel(
            name="PeriodicTask",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Useful description",
                        max_length=200,
                        unique=True,
                        verbose_name="name",
                    ),
                ),
                ("task", models.CharField(max_length=200, verbose_name="task name")),
                (
                    "args",
                    models.TextField(
                        blank=True,
                        default="[]",
                        help_text="JSON encoded positional arguments",
                        verbose_name="Arguments",
                    ),
                ),
                (
                    "kwargs",
                    models.TextField(
                        blank=True,
                        default="{}",
                        help_text="JSON encoded keyword arguments",
                        verbose_name="Keyword arguments",
                    ),
                ),
                (
                    "queue",
                    models.CharField(
                        blank=True,
                        default=None,
                        help_text="Queue defined in CELERY_TASK_QUEUES",
                        max_length=200,
                        null=True,
                        verbose_name="queue",
                    ),
                ),
                (
                    "exchange",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=200,
                        null=True,
                        verbose_name="exchange",
                    ),
                ),
                (
                    "routing_key",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=200,
                        null=True,
                        verbose_name="routing key",
                    ),
                ),
                (
                    "expires",
                    models.DateTimeField(blank=True, null=True, verbose_name="expires"),
                ),
                ("enabled", models.BooleanField(default=True, verbose_name="enabled")),
                (
                    "last_run_at",
                    models.DateTimeField(blank=True, editable=False, null=True),
                ),
                (
                    "total_run_count",
                    models.PositiveIntegerField(default=0, editable=False),
                ),
                ("date_changed", models.DateTimeField(auto_now=True)),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                (
                    "crontab",
                    models.ForeignKey(
                        blank=True,
                        help_text="Use one of interval/crontab",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_celery_beat.CrontabSchedule",
                        verbose_name="crontab",
                    ),
                ),
                (
                    "interval",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_celery_beat.IntervalSchedule",
                        verbose_name="interval",
                    ),
                ),
            ],
            options={
                "verbose_name": "periodic task",
                "verbose_name_plural": "periodic tasks",
            },
        ),
        migrations.CreateModel(
            name="PeriodicTasks",
            fields=[
                (
                    "ident",
                    models.SmallIntegerField(
                        default=1, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("last_update", models.DateTimeField()),
            ],
        ),
    ]
