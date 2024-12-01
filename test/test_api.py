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
	assert response_json["material"] == input_data["material"]
	assert response_json["description"] == input_data["description"]
	assert response_json["weight"] == str(input_data["weight"])
	assert response_json["weight_uom"] == "KG"
	assert response_json["volume"] == str(input_data["volume"])
	assert response_json["volume_uom"] == "CDM"
	assert response_json["created_by"] is not None
	assert response_json["created_on"] is not None
	logging.info("Creation material testing finished.")
	os.environ["MATERIAL_ID"] = str(response_json["id_material"])


def sub_test_update_material(client, input_data):
	id_material = int(os.environ["MATERIAL_ID"])
	url = reverse("materials-detail", kwargs={"pk": id_material})
	response = client.put(path=url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Update material testing ...")
	assert response.status_code == 200
	assert response_json["description"] == input_data["description"]
	assert response_json["weight"] == str(input_data["weight"])
	assert response_json["weight_uom"] == input_data["weight_uom"]
	assert response_json["volume"] == str(input_data["volume"])
	assert response_json["volume_uom"] == input_data["volume_uom"]
	assert response_json["created_by"] is not None
	assert response_json["created_on"] is not None
	logging.info("Update material testing finished.")


def sub_test_delete_material(client):
	id_material = int(os.environ["MATERIAL_ID"])
	url = reverse("materials-detail", kwargs={"pk": id_material})
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
	assert response_json["id_bin"] == input_data["id_bin"]
	assert response_json["type"] == "ST"
	assert response_json["verification_field"] == input_data["verification_field"]
	assert response_json["handlingunit"] is None
	assert response_json["empty"] is True
	logging.info("Creation bin testing finished.")
	os.environ["BIN_ID"] = str(response_json["id_bin"])


def sub_test_update_bin(client, input_data):
	id_bin = os.environ["BIN_ID"]
	url = reverse("bins-detail", kwargs={"pk": id_bin})
	response = client.put(path=url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Update bin testing ...")
	assert response.status_code == 200
	assert response_json["id_bin"] == id_bin
	assert response_json["type"] == input_data["type"]
	assert response_json["verification_field"] == input_data["verification_field"]
	assert response_json["handlingunit"] is None
	assert response_json["empty"] is True
	assert response_json["created_by"] is not None
	assert response_json["created_on"] is not None
	logging.info("Update bin testing finished.")


def sub_test_delete_bin(client):
	id_bin = os.environ["BIN_ID"]
	url = reverse("bins-detail", kwargs={"pk": id_bin})
	response = client.delete(path=url)
	response_json = response.json()
	logging.info("Deletion bin testing ...")
	assert response.status_code == 200
	assert response_json == {"message": "Bin has been deleted."}
	logging.info("Deletion bin testing finished.")


def sub_test_goods_receipt(client, input_data):
	url = reverse("goodsreceipts-list")
	response = client.post(path=url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Goods Receipt testing ...")
	assert response.status_code == 200
	assert response_json == {"message": "Goods Receipt completed."}
	logging.info("Goods Receipt testing finished.")


def sub_test_create_task(client, input_data):
	url = reverse("tasks-list")
	response = client.get(path=url)
	response_json = response.json()["results"][0]
	logging.info("Creation task testing ...")
	assert response.status_code == 200
	assert response_json["handlingunit"] is not None
	assert response_json["source_bin"] == "GR-ZONE"
	assert response_json["destination_bin"] == input_data["id_bin"]
	assert response_json["created_by"] is not None
	assert response_json["created_on"] is not None
	logging.info("Creation task finished.")
	os.environ["HU_ID"] = str(response_json["handlingunit"])
	os.environ["BIN_ID"] = input_data["id_bin"]


def sub_test_goods_issue(client):
	id_handlingunit = int(os.environ["HU_ID"])
	id_bin = os.environ["BIN_ID"]

	url = reverse("goodsissues-list")
	input_data = {"handlingunit": id_handlingunit}
	response = client.post(path=url, data=input_data, format="json")
	response_json = response.json()

	url_hu = reverse("handlingunits-detail", kwargs={"pk": id_handlingunit})
	response_hu = client.get(path=url_hu)
	response_json_hu = response_hu.json()

	url_bin = reverse("bins-detail", kwargs={"pk": id_bin})
	response_bin = client.get(path=url_bin)
	response_json_bin = response_bin.json()

	logging.info("Goods Issue testing ...")
	assert response.status_code == 200
	assert response_json == {"message": "Goods Issue completed."}
	assert response_hu.status_code == 200
	assert response_json_hu["is_active"] == False
	assert response_bin.status_code == 200
	assert response_json_bin["handlingunit"] is None
	assert response_json_bin["empty"] == True
	logging.info("Goods Issue testing finished.")


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


def test_flow(
					client_test,
					data_test_create_material,
					data_test_create_bin,
					data_test_goods_receipt):
	logging.info("START - flow testing")
	sub_test_create_material(client_test, data_test_create_material)
	sub_test_create_bin(client_test, data_test_create_bin)
	sub_test_goods_receipt(client_test, data_test_goods_receipt)
	sub_test_create_task(client_test, data_test_create_bin)
	sub_test_goods_issue(client_test)
	logging.info("STOP - flow testing")
