# -*- coding: utf-8 -*-

from django_filters.rest_framework import FilterSet, CharFilter, DateFilter, NumberFilter


class MaterialFilter(FilterSet):
    material = CharFilter(field_name="material", lookup_expr="icontains")
    description = CharFilter(field_name="description", lookup_expr="icontains")


class TaskFilter(FilterSet):
    id_task = NumberFilter(field_name="id_task", lookup_expr="exact")
    handlingunit = NumberFilter(field_name="handlingunit", lookup_expr="exact")
    source_bin = CharFilter(field_name="source_bin__id_bin", lookup_expr="istartswith")
    destination_bin = CharFilter(field_name="destination_bin__id_bin", lookup_expr="istartswith")
    created_by = CharFilter(field_name="created_by", lookup_expr="iexact")
    created_on = DateFilter(field_name="created_on", lookup_expr="date__iexact")
