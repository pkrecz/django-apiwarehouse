# -*- coding: utf-8 -*-

from django.apps import AppConfig


class AppApiwhsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_apiwhs"

    def ready(self):
        import app_apiwhs.initdata
