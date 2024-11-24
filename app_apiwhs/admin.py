# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import MaterialModel, HandlingUnitModel, BinModel, TaskModel


admin.site.register(MaterialModel)
admin.site.register(HandlingUnitModel)
admin.site.register(BinModel)
admin.site.register(TaskModel)
