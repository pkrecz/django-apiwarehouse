# -*- coding: utf-8 -*-

from rest_framework.exceptions import APIException
from .models import MaterialModel, BinModel, TaskModel
from .serializers import HandlingUnitCreateSerializer


def get_material_master_data(material):
    instance = MaterialModel.objects.filter(material=material)
    if not instance.exists():
        raise APIException(detail={"message": "Material was not found."})
    master_data = instance.values(  
                                    "id_material",
                                    "weight",
                                    "weight_uom",
                                    "volume",
                                    "volume_uom")
    master_data = master_data.first()
    return dict(master_data)


def create_handling_unit(material, quantity):
    master_data = get_material_master_data(material)
    data = dict()
    data["material"] = master_data["id_material"]
    data["quantity"] = quantity
    data["weight"] = master_data["weight"] * quantity
    data["weight_uom"] = master_data["weight_uom"]
    data["volume"] = master_data["volume"] * quantity
    data["volume_uom"] = master_data["volume_uom"]
    serializer = HandlingUnitCreateSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    return instance


def get_next_empty_bin():
    instance = BinModel.objects.filter(empty=True).order_by("id_bin")
    if not instance.exists():
        raise APIException(detail={"message": "No empty bin."})
    instance = instance.first()
    return instance


def get_GR_ZONE_bin():
    instance = BinModel.objects.filter(id_bin="GR-ZONE")
    if not instance.exists():
        raise APIException(detail={"message": "Bin 'GR-ZONE' was not found."})
    instance = instance.first()
    return instance


def set_bin_occupied(bin, handlingunit):
    bin.empty = False
    bin.handlingunit = handlingunit
    bin.save()




def set_bin_empty(bin, handlingunit):
    pass




def create_task(request, handlingunit, source, destination):
    try:
        instance = TaskModel.objects.create(
                                            handlingunit=handlingunit,
                                            source_bin=source,
                                            destination_bin=destination,
                                            created_by=request.user)
        return instance
    except:
        raise APIException(detail={"message": "Error in warehouse creation."})
