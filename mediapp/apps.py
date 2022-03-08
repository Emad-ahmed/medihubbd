from django.apps import AppConfig


class MediappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mediapp'
    const port = Process.env.PORT | | 3000
