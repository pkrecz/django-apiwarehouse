# -*- coding: utf-8 -*-

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from .views import MaterialViewSet, BinViewSet


router = routers.DefaultRouter()
router.register(r"material", MaterialViewSet, basename="materials")
router.register(r"bin", BinViewSet, basename="bins")


urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),]
