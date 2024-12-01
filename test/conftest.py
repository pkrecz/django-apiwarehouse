# -*- coding: utf-8 -*-

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


# Preparing envoirment for testing
@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db): 
    pass


@pytest.fixture()
def db_access_without_rollback_and_truncate(request, django_db_setup, django_db_blocker):
    django_db_blocker.unblock()
    yield
    django_db_blocker.restore()


@pytest.fixture()
def client_test():
    user = User.objects.create_superuser(username="test_user", password="test_password")
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client


# Preparing sample data
@pytest.fixture()
def data_test_create_material():
    return {
            "material": "BDP100I",
            "description": "Metronomis gen. 2",
            "weight": 1.25,
            "volume": 0.65}


@pytest.fixture()
def data_test_update_material():
    return {
            "description": "Metronomis gen. 2 100W",
            "weight": 1000.45,
            "weight_uom": "G",
            "volume": 0.08,
            "volume_uom": "M3"}


@pytest.fixture()
def data_test_create_bin():
    return {
            "id_bin": "0510-P05-A4",
            "verification_field": "xYz123@"}


@pytest.fixture()
def data_test_update_bin():
    return {
            "type": "EL",
            "verification_field": "ABc123!"}


@pytest.fixture()
def data_test_goods_receipt():
    return {
            "material": "BDP100I",
            "quantity": 3}
