# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import MaterialModel, BinModel, HandlingUnitModel, TaskModel


""" Material """
class MaterialCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialModel
        fields = "__all__"
        read_only_fields = ["created_by", "created_on"]


class MaterialUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialModel
        fields = "__all__"
        read_only_fields = ["material", "created_by", "created_on"]


class MaterialLRDSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialModel
        fields = "__all__"


""" Bin """
class BinCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BinModel
        fields = "__all__"
        read_only_fields = ["handlingunit", "empty", "created_by", "created_on"]


class BinUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BinModel
        fields = "__all__"
        read_only_fields = ["id_bin", "handlingunit", "empty", "created_by", "created_on"]


class BinLRDSerializer(serializers.ModelSerializer):

    class Meta:
        model = BinModel
        fields = "__all__"


""" HandlingUnit """
class HandlingUnitCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HandlingUnitModel
        fields = "__all__"
        read_only_fields = ["is_active"]


class HandlingUnitLRSerializer(serializers.ModelSerializer):

    class Meta:
        model = HandlingUnitModel
        fields = "__all__"


""" Task """
class TaskLRSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskModel
        fields = "__all__"


""" GoodsReceipt """
class GoodsReceiptSerializer(serializers.Serializer):

    material = serializers.RegexField(
                                        max_length=12,
                                        regex="^[0-9A-Z]*$")
    quantity = serializers.IntegerField(
                                        min_value=1)
