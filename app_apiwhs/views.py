# -*- coding: utf-8 -*-


import datetime
import decimal
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.db import transaction
from django.db.models import ProtectedError
from collections import OrderedDict
from drf_yasg.utils import swagger_auto_schema
from .models import MaterialModel, BinModel
from .serializers import (MaterialCreateSerializer, MaterialUpdateSerializer, MaterialLRDSerializer,
                          BinCreateSerializer, BinUpdateSerializer, BinLRDSerializer)


""" Material """
class MaterialViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = MaterialModel.objects.all()
    #filterset_class = CustomerFilter
    #search_fields = ["pesel", "identification"]
    #ordering_fields = ["last_name", "first_name"]
    #ordering = ["last_name"]

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
        except APIException as exc:
            return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)

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
        except APIException as exc:
            return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)


""" Bin """
class BinViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = BinModel.objects.all()

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
        except APIException as exc:
            return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)

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
        except APIException as exc:
            return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)
