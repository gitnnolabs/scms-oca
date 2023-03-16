# Generated by Django 3.2.12 on 2022-08-29 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("usefulmodels", "0001_initial"),
        ("taggit", "0004_alter_taggeditem_content_type_alter_taggeditem_tag"),
        ("wagtaildocs", "0012_uploadeddocument"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("institution", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="InfrastructureDirectoryFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Data de criação"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Data da última atualização"
                    ),
                ),
                (
                    "is_valid",
                    models.BooleanField(
                        blank=True, default=False, null=True, verbose_name="É válido"
                    ),
                ),
                (
                    "line_count",
                    models.IntegerField(
                        blank=True,
                        default=0,
                        null=True,
                        verbose_name="Número de linhas",
                    ),
                ),
                (
                    "attachment",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtaildocs.document",
                        verbose_name="Anexo",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="infrastructuredirectoryfile_creator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Criador",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="infrastructuredirectoryfile_last_mod_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Atualizador",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Diretório de Infraestrutura Upload",
            },
        ),
        migrations.CreateModel(
            name="InfrastructureDirectory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Data de criação"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Data da última atualização"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Título")),
                ("link", models.URLField(verbose_name="Link")),
                (
                    "description",
                    models.TextField(
                        blank=True, max_length=1000, null=True, verbose_name="Descrição"
                    ),
                ),
                (
                    "classification",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", ""),
                            ("portal", "Portal"),
                            ("plataforma", "Plataforma"),
                            ("servidor", "Servidor"),
                            ("repositório", "Repositório"),
                            ("serviço", "Serviço"),
                            ("outras", "Outras"),
                        ],
                        max_length=255,
                        null=True,
                        verbose_name="Classificação",
                    ),
                ),
                (
                    "record_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", ""),
                            ("WIP", "WIP"),
                            ("TO_MODERATE", "TO_MODERATE"),
                            ("PUBLISHED", "PUBLISHED"),
                        ],
                        max_length=255,
                        null=True,
                        verbose_name="Record status",
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Origem"
                    ),
                ),
                (
                    "action",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="usefulmodels.action",
                        verbose_name="Ação",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="infrastructuredirectory_creator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Criador",
                    ),
                ),
                (
                    "institutions",
                    models.ManyToManyField(
                        blank=True,
                        to="institution.Institution",
                        verbose_name="Instituição",
                    ),
                ),
                (
                    "keywords",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Palavra-chave",
                    ),
                ),
                (
                    "practice",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="usefulmodels.practice",
                        verbose_name="Practice",
                    ),
                ),
                (
                    "thematic_areas",
                    models.ManyToManyField(
                        blank=True,
                        to="usefulmodels.ThematicArea",
                        verbose_name="Área temática",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="infrastructuredirectory_last_mod_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Atualizador",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Diretório de Infraestrutura",
            },
        ),
    ]
