from django.contrib import admin
from .models import *
from django.apps import apps


app_models = apps.get_app_config('api').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
