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
                          GoodsReceiptSerializer, GoodsIssueSerializer, MovementSerializer)
from .filters import MaterialFilter, TaskFilter
from .functions import (create_handling_unit, create_task,
                        get_next_empty_bin_instance, set_bin_occupied, set_bin_empty, get_bin_instance,
                        get_handlingunit_location_instance, get_handlingunit_instance, set_handlingunit_inactive)


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
                material = serializer.validated_data.get("material")
                quantity = serializer.validated_data.get("quantity")
                handlingunit_instance = create_handling_unit(
                                                                material=material,
                                                                quantity=quantity)
                empty_bin_instance = get_next_empty_bin_instance()
                gr_zone_bin_instance = get_bin_instance("GR-ZONE")
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


""" GoodsIssue """
class GoodsIssueViewSet(viewsets.GenericViewSet):
    http_method_names = ["post"]
    serializer_class = GoodsIssueSerializer
    swagger_viewset_tag = ["Goods Issue"]

    def create(self, request):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                id_handlingunit = serializer.validated_data.get("handlingunit")
                bin_instance = get_handlingunit_location_instance(id_handlingunit)
                handlingunit_instance = get_handlingunit_instance(id_handlingunit)
                gi_zone_bin_instance = get_bin_instance("GI-ZONE")
                create_task(
                                request=request,
                                handlingunit=handlingunit_instance,
                                source=bin_instance,
                                destination=gi_zone_bin_instance)
                set_bin_empty(bin=bin_instance)
                set_handlingunit_inactive(handlingunit=handlingunit_instance)
                return JsonResponse(data={"message": "Goods Issue completed."}, status=status.HTTP_200_OK)
        except APIException as exception:
            return JsonResponse(data=exception.detail, status=status.HTTP_400_BAD_REQUEST)


""" Movement """
class MovementViewSet(viewsets.GenericViewSet):
    http_method_names = ["post"]
    serializer_class = MovementSerializer
    swagger_viewset_tag = ["Movement"]

    def create(self, request):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                handlingunit_instance = serializer.validated_data.get("handlingunit")
                source_bin_instance = get_handlingunit_location_instance(handlingunit_instance.id_handlingunit)
                destination_bin_instance = serializer.validated_data.get("destination_bin")
                if destination_bin_instance.empty == False:
                    raise APIException(detail={"message": "Destination bin is occupied."})
                create_task(
                                request=request,
                                handlingunit=handlingunit_instance,
                                source=source_bin_instance,
                                destination=destination_bin_instance)
                set_bin_empty(bin=source_bin_instance)
                set_bin_occupied(
                                bin=destination_bin_instance,
                                handlingunit=handlingunit_instance)
                return JsonResponse(data={"message": "Movement completed."}, status=status.HTTP_200_OK)
        except APIException as exception:
            return JsonResponse(data=exception.detail, status=status.HTTP_400_BAD_REQUEST)
