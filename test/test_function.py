# -*- coding: utf-8 -*-

import os
import logging
from decimal import Decimal
from django.urls import reverse
from .test_api import sub_test_create_material
from app_apiwhs import functions


def sub_test_get_material_master_data(material):
    data = functions.get_material_master_data(material)
    logging.info("Getting material master data testing ...")
    assert data["id_material"] is not None
    assert data["weight"] == Decimal("1.25")
    assert data["weight_uom"] == "KG"
    assert data["volume"] == Decimal("0.65")
    assert data["volume_uom"] == "CDM"
    logging.info("Getting material master data finished.")
    os.environ["MATERIAL_ID"] = str(data["id_material"] )


def sub_test_create_handling_unit(client, material, quantity):
    id_material = int(os.environ["MATERIAL_ID"])
    handlingunit_instance = functions.create_handling_unit(material, quantity)
    id_handlingunit = int(handlingunit_instance.id_handlingunit)
    url = reverse("handlingunits-detail", kwargs={"pk": id_handlingunit})
    response = client.get(path=url)
    response_json = response.json()
    logging.info("Creation handling unit testing ...")
    assert id_handlingunit is not None
    assert response_json["quantity"] == quantity
    assert response_json["weight"] == str(Decimal("1.25") * quantity)
    assert response_json["weight_uom"] == "KG"
    assert response_json["volume"] == str(Decimal("0.65") * quantity)
    assert response_json["volume_uom"] == "CDM"
    assert response_json["is_active"] == True
    assert response_json["material"] == id_material
    logging.info("Creation handling unit finished.")


# Test to be performed.
def test_functions(
                    client_test,
					data_test_create_material,
                    data_test_goods_receipt):
    logging.info("START - functions testing")
    sub_test_create_material(client_test, data_test_create_material)
    sub_test_get_material_master_data(data_test_create_material["material"])
    sub_test_create_handling_unit(client_test, data_test_create_material["material"], data_test_goods_receipt["quantity"])
    logging.info("STOP - functions testing")
