# -*- coding: utf-8 -*-

import os
import logging
from django.urls import reverse


def sub_test_create_material(client, input_data):
	url = reverse("materials-list")
	response = client.post(path=url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Creation material testing ...")
	assert response.status_code == 201
	assert response_json["material"] == "BDP100I"
	assert response_json["description"] == "Metronomis gen. 2"
	assert response_json["weight"] == "1.25"
	assert response_json["weight_uom"] == "KG"
	assert response_json["volume"] == "0.65"
	assert response_json["volume_uom"] == "CDM"
	assert response_json["created_by"] is not None
	assert response_json["created_on"] is not None
	logging.info("Creation material testing finished.")
	os.environ["MATERIAL_ID"] = str(response_json["id_material"])


def sub_test_update_material(client, input_data):
	id_material = os.environ["MATERIAL_ID"]
	url = reverse("materials-detail", kwargs={"pk": int(id_material)})
	response = client.put(path=url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Update material testing ...")
	assert response.status_code == 200
	assert response_json["material"] == "BDP100I"
	assert response_json["description"] == "Metronomis gen. 2 100W"
	assert response_json["weight"] == "1000.45"
	assert response_json["weight_uom"] == "G"
	assert response_json["volume"] == "0.08"
	assert response_json["volume_uom"] == "M3"
	assert response_json["created_by"] is not None
	assert response_json["created_on"] is not None
	logging.info("Update material testing finished.")


def sub_test_delete_material(client):
	id_material = os.environ["MATERIAL_ID"]
	url = reverse("materials-detail", kwargs={"pk": int(id_material)})
	response = client.delete(path=url)
	response_json = response.json()
	logging.info("Deletion material testing ...")
	assert response.status_code == 200
	assert response_json == {"message": "Material has been deleted."}
	logging.info("Deletion material testing finished.")


def sub_test_create_bin(client, input_data):
	url = reverse("bins-list")
	response = client.post(path=url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Creation bin testing ...")
	assert response.status_code == 201
	assert response_json["id_bin"] == "0510-P05-A4"
	assert response_json["type"] == "ST"
	assert response_json["verification_field"] == "xYz123@"
	assert response_json["hu"] is None
	assert response_json["empty"] is True
	logging.info("Creation bin testing finished.")
	os.environ["BIN_ID"] = str(response_json["id_bin"])


def sub_test_update_bin(client, input_data):
	id_bin = os.environ["BIN_ID"]
	url = reverse("bins-detail", kwargs={"pk": str(id_bin)})
	response = client.put(path=url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Update bin testing ...")
	assert response.status_code == 200
	assert response_json["id_bin"] == "0510-P05-A4"
	assert response_json["type"] == "EL"
	assert response_json["verification_field"] == "ABc123!"
	assert response_json["hu"] is None
	assert response_json["empty"] is True
	assert response_json["created_by"] is not None
	assert response_json["created_on"] is not None
	logging.info("Update bin testing finished.")


def sub_test_delete_bin(client):
	id_bin = os.environ["BIN_ID"]
	url = reverse("bins-detail", kwargs={"pk": str(id_bin)})
	response = client.delete(path=url)
	response_json = response.json()
	logging.info("Deletion bin testing ...")
	assert response.status_code == 200
	assert response_json == {"message": "Bin has been deleted."}
	logging.info("Deletion bin testing finished.")


# Test to be performed.
def test_model(
					client_test,
					data_test_create_material,
					data_test_update_material,
					data_test_create_bin,
					data_test_update_bin):
	logging.info("START - model testing")
	sub_test_create_material(client_test, data_test_create_material)
	sub_test_update_material(client_test, data_test_update_material)
	sub_test_delete_material(client_test)
	sub_test_create_bin(client_test, data_test_create_bin)
	sub_test_update_bin(client_test, data_test_update_bin)
	sub_test_delete_bin(client_test)
	logging.info("STOP - model testing")
