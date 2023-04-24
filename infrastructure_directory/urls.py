from django.urls import path

from .views import import_file, validate, download_sample


app_name = "infrastructure_directory"
urlpatterns = [
    path("validate", view=validate, name="validate"),
    path("import", view=import_file, name="import_file"),
    path("download", view=download_sample, name="download_sample"),
]
