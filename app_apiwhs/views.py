# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework import status
from rest_framework.exceptions import APIException
from django.http import JsonResponse
from django.db import transaction
from django.db.models import ProtectedError
from .models import MaterialModel, BinModel, HandlingUnitModel, TaskModel
from .serializers import (MaterialCreateSerializer, MaterialUpdateSerializer, MaterialLRDSerializer,
                          BinCreateSerializer, BinUpdateSerializer, BinLRDSerializer,
                          HandlingUnitLRSerializer,
                          TaskLRSerializer,
                          GoodsReceiptSerializer)
from .filters import MaterialFilter, TaskFilter
from .functions import (create_handling_unit, create_task,
                        get_next_empty_bin, set_bin_occupied, set_bin_empty, get_GR_ZONE_bin)


""" Material """
class MaterialViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = MaterialModel.objects.all()
    filterset_class = MaterialFilter
    search_fields = ["material", "description"]
    ordering_fields = ["material", "description"]
    ordering = ["material"]
    swagger_viewset_tag = ["Material"]

    def get_serializer_class(self):
        match self.action:
            case "create":
                return MaterialCreateSerializer
            case "update":
                return MaterialUpdateSerializer
            case _:
                return MaterialLRDSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save(created_by=self.request.user)
            return_serializer = MaterialLRDSerializer(instance, context={"request": request})
            return JsonResponse(data=return_serializer.data, status=status.HTTP_201_CREATED)
        except APIException as exception:
            return JsonResponse(data=exception.detail, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return JsonResponse(data={"message": "Material has been deleted."}, status=status.HTTP_200_OK)
        except ProtectedError:
            return JsonResponse(data={"message": "Deletion impossible. This record has referenced data!"}, status=status.HTTP_400_BAD_REQUEST)
        except APIException as exception:
            return JsonResponse(data=exception.detail, status=status.HTTP_400_BAD_REQUEST)


""" Bin """
class BinViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = BinModel.objects.all()
    swagger_viewset_tag = ["Bin"]

    def get_serializer_class(self):
        match self.action:
            case "create":
                return BinCreateSerializer
            case "update":
                return BinUpdateSerializer
            case _:
                return BinLRDSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save(created_by=self.request.user)
            return_serializer = BinLRDSerializer(instance, context={"request": request})
            return JsonResponse(data=return_serializer.data, status=status.HTTP_201_CREATED)
        except APIException as exception:
            return JsonResponse(data=exception.detail, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return JsonResponse(data={"message": "Bin has been deleted."}, status=status.HTTP_200_OK)
        except ProtectedError:
            return JsonResponse(data={"message": "Deletion impossible. This record has referenced data!"}, status=status.HTTP_400_BAD_REQUEST)
        except APIException as exception:
            return JsonResponse(data=exception.detail, status=status.HTTP_400_BAD_REQUEST)


""" HandlingUnit """
class HandlingUnitViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = HandlingUnitLRSerializer
    queryset = HandlingUnitModel.objects.all()
    swagger_viewset_tag = ["Handling Unit"]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


""" Task """
class TaskViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = TaskLRSerializer
    queryset = TaskModel.objects.all()
    filterset_class = TaskFilter
    swagger_viewset_tag = ["Warehouse Task"]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


""" GoodsReceipt """
class GoodsReceiptViewSet(viewsets.GenericViewSet):
    http_method_names = ["post"]
    serializer_class = GoodsReceiptSerializer
    swagger_viewset_tag = ["Goods Receipt"]

    def create(self, request):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                handlingunit_instance = create_handling_unit(
                                                    material=serializer.validated_data["material"],
                                                    quantity=serializer.validated_data["quantity"])
                empty_bin_instance = get_next_empty_bin()
                gr_zone_bin_instance = get_GR_ZONE_bin()
                create_task(
                                request=request,
                                handlingunit=handlingunit_instance,
                                source=gr_zone_bin_instance,
                                destination=empty_bin_instance)
                set_bin_occupied(
                                bin=empty_bin_instance,
                                handlingunit=handlingunit_instance)
                return JsonResponse(data={"message": "Goods Receipt completed."}, status=status.HTTP_200_OK)
        except APIException as exception:
            return JsonResponse(data=exception.detail, status=status.HTTP_400_BAD_REQUEST)
