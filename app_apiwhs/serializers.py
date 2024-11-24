# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import MaterialModel, BinModel


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
        read_only_fields = ["hu", "empty", "created_by", "created_on"]


class BinUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BinModel
        fields = "__all__"
        read_only_fields = ["id_bin", "hu", "empty", "created_by", "created_on"]


class BinLRDSerializer(serializers.ModelSerializer):

    class Meta:
        model = BinModel
        fields = "__all__"
