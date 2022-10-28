from django.shortcuts import render
from django.http import HttpResponse
import xlrd
import os
from .models import *
from rest_framework import viewsets
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from rest_framework import serializers


def fill_values(request):
    file_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + "/New Insect Business List.xlsx"
    wb = xlrd.open_workbook(file_path)
    total_sheets = wb.sheet_names()
    sheet = wb.sheet_by_index(2)
    # for i in range(19,sheet.ncols-1):
    #     obj = Species.objects.create(name = sheet.cell_value(0, i))
    #     print(obj.name)

    for i in range(1,sheet.nrows):
        print(i)
        obj = InsectBusiness.objects.create(brand_name=sheet.cell_value(i, 0))
        obj.parent_company = sheet.cell_value(i, 1)
        obj.home_country, created = HomeCountry.objects.get_or_create(name=sheet.cell_value(i, 2))
        obj.updated = sheet.cell_value(i, 3)

        if sheet.cell_value(i,4) == "":
            obj.active = "NOT ASSIGNED"
        else:
            obj.active = sheet.cell_value(i,4)

        if sheet.cell_value(i,5) == "":
            obj.farm = "NOT ASSIGNED"
        else:
            obj.farm = sheet.cell_value(i,5)

        if sheet.cell_value(i,6) == "":
            obj.end_product = "NOT ASSIGNED"
        else:
            obj.end_product = sheet.cell_value(i,6)

        if sheet.cell_value(i,7) == "" or sheet.cell_value(i,7) == "-":
            obj.primary_focus = Focus.objects.get(name="NOT ASSIGNED")
        else:
            obj.primary_focus, created = Focus.objects.get_or_create(name=sheet.cell_value(i, 7))

        if sheet.cell_value(i,8) == "" or sheet.cell_value(i,8) == "-":
            obj.secondary_focus = Focus.objects.get(name="NOT ASSIGNED")
        else:
            obj.secondary_focus, created = Focus.objects.get_or_create(name=sheet.cell_value(i, 8))


        if sheet.cell_value(i, 9) == "":
            obj.date_began = sheet.cell_value(i, 9)
        else:
            try:
                obj.date_began = int(sheet.cell_value(i, 9))
            except Exception as e:
                obj.date_began = sheet.cell_value(i, 9)

        obj.mailing_address = sheet.cell_value(i, 10)
        obj.street_address = sheet.cell_value(i, 11)
        obj.postal_code = sheet.cell_value(i, 12)
        obj.city = sheet.cell_value(i, 13)
        obj.state = sheet.cell_value(i, 14)
        obj.contact_name = sheet.cell_value(i, 15)
        obj.email = sheet.cell_value(i, 16)
        obj.phone_number = sheet.cell_value(i, 17)

        for j in range(19,sheet.ncols-1):
            if len(str(sheet.cell_value(i,j))) != 0 and sheet.cell_value(i,j) != 0:
                obj.species.add(Species.objects.get(name=sheet.cell_value(0,j)))
        obj.save()

        # if i> 100:
        #     return HttpResponse("Done")


    return HttpResponse("Done")


def startapp(request):
    return render(request,'index.html',)


class HomeCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeCountry
        fields = ['name']

class FocusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Focus
        fields = ['name']


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ['name']

class InsectBusinessSerializer(serializers.ModelSerializer):
    species = SpeciesSerializer(many=True)
    home_country = HomeCountrySerializer(many=False)
    primary_focus = FocusSerializer(many=False)
    secondary_focus = FocusSerializer(many=False)

    class Meta:
        model = InsectBusiness
        fields = '__all__'

class InsectBusinessFilter(filters.FilterSet):
    species = filters.ModelMultipleChoiceFilter(
        field_name='species__name',
        to_field_name='name',
        queryset=Species.objects.all(),
        conjoined=True
    )
    home_country = filters.ModelMultipleChoiceFilter(
        field_name='home_country__name',
        to_field_name='name',
        queryset=HomeCountry.objects.all(),
        conjoined = False
    )
    primary_focus = filters.ModelMultipleChoiceFilter(
        field_name='primary_focus__name',
        to_field_name='name',
        queryset=Focus.objects.all(),
        conjoined = False
    )
    secondary_focus = filters.ModelMultipleChoiceFilter(
        field_name='secondary_focus__name',
        to_field_name='name',
        queryset=Focus.objects.all(),
        conjoined = False
    )

    class Meta:
        model = InsectBusiness
        fields = ['active','farm','end_product','home_country','primary_focus','secondary_focus','species']



class HomeCountryAPI(viewsets.ModelViewSet):
    queryset = HomeCountry.objects.all()
    serializer_class = HomeCountrySerializer
    filter_backends = [filters.DjangoFilterBackend,SearchFilter]
    search_fields = ['name']

class FocusAPI(viewsets.ModelViewSet):
    queryset = Focus.objects.all()
    serializer_class = FocusSerializer
    filter_backends = [filters.DjangoFilterBackend,SearchFilter]
    search_fields = ['name']

class SpeciesAPI(viewsets.ModelViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    filter_backends = [filters.DjangoFilterBackend,SearchFilter]
    search_fields = ['name']


class InsectBusinessAPI(viewsets.ModelViewSet):
    queryset = InsectBusiness.objects.all()
    serializer_class = InsectBusinessSerializer
    filter_backends = [filters.DjangoFilterBackend,SearchFilter]
    filterset_class = InsectBusinessFilter
    search_fields = ['brand_name', 'parent_company','mailing_address', 'street_address', 'postal_code', 'city', 'state','contact_name','email','phone_number']
