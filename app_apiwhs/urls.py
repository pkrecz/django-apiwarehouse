# -*- coding: utf-8 -*-

from django.urls import path, include
from rest_framework import routers
from .views import MaterialViewSet, BinViewSet, HandlingUnitViewSet, TaskViewSet, GoodsReceiptViewSet


router = routers.DefaultRouter()
router.register(r"material", MaterialViewSet, basename="materials")
router.register(r"bin", BinViewSet, basename="bins")
router.register(r"handlingunit", HandlingUnitViewSet, basename="handlingunits")
router.register(r"task", TaskViewSet, basename="tasks")
router.register(r"goodsreceipt", GoodsReceiptViewSet, basename="goodsreceipts")


urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),]
