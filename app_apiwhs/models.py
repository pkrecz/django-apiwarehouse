# -*- coding: utf-8 -*-

from decimal import Decimal
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator


""" Material Model """
class MaterialModel(models.Model):

    id_material = models.AutoField(
                                primary_key=True)
    material = models.CharField(
                                unique=True,
                                max_length=12,
                                validators=[RegexValidator(regex="^[0-9A-Z]*$")])
    description = models.CharField(
                                max_length=200)
    weight = models.DecimalField(
                                max_digits=9,
                                decimal_places=2,
                                validators=[MinValueValidator(Decimal(0.01))])
    weight_uom = models.CharField(
                                max_length=2,
                                default="KG")
    volume = models.DecimalField(
                                max_digits=6,
                                decimal_places=2,
                                validators=[MinValueValidator(Decimal(0.01))])
    volume_uom = models.CharField(
                                max_length=3,
                                default="CDM")
    created_by = models.CharField(
                                max_length=50)
    created_on = models.DateTimeField(
                                auto_now_add=True)

    def save(self, *args, **kwargs):
        self.material = self.material.upper()
        self.weight_uom = self.weight_uom.upper()
        self.volume_uom = self.volume_uom.upper()
        super().save(*args, **kwargs)


""" HandlingUnit Model """
class HandlingUnitModel(models.Model):

    id_handlingunit = models.AutoField(
                                primary_key=True)
    material = models.ForeignKey(
                                to="MaterialModel",
                                related_name="material_hu",
                                on_delete=models.PROTECT)
    quantity = models.IntegerField(
                                validators=[MinValueValidator(1)])
    weight = models.DecimalField(
                                max_digits=9,
                                decimal_places=2)
    weight_uom = models.CharField(
                                max_length=2)
    volume = models.DecimalField(
                                max_digits=6,
                                decimal_places=2)
    volume_uom = models.CharField(
                                max_length=3)
    is_active = models.BooleanField(
                                default="True")


""" Bin Model """
class BinModel(models.Model):

    id_bin = models.CharField(
                                primary_key=True,
                                max_length=15,
                                validators=[RegexValidator(regex="^[0-9A-Z-]*$")])
    type = models.CharField(
                                max_length=3,
                                default="ST")
    verification_field = models.CharField(
                                max_length=15,
                                blank=True,
                                null=True)
    handlingunit = models.OneToOneField(
                                to="HandlingUnitModel",
                                related_name="bin_hu",
                                blank=True,
                                null=True,
                                on_delete=models.PROTECT)
    empty = models.BooleanField(
                                default="True")
    created_by = models.CharField(
                                max_length=50)
    created_on = models.DateTimeField(
                                auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id_bin = self.id_bin.upper()
        self.type = self.type.upper()
        super().save(*args, **kwargs)


""" Task Model """
class TaskModel(models.Model):

    id_task = models.AutoField(
                                primary_key=True)
    handlingunit = models.ForeignKey(
                                to="HandlingUnitModel",
                                related_name="task_hu",
                                on_delete=models.PROTECT)
    source_bin = models.ForeignKey(
                                to="BinModel",
                                related_name="task_source_bin",
                                on_delete=models.PROTECT)
    destination_bin = models.ForeignKey(
                                to="BinModel",
                                related_name="task_destination_bin",
                                on_delete=models.PROTECT)
    created_by = models.CharField(
                                max_length=50)
    created_on = models.DateTimeField(
                                auto_now_add=True)
