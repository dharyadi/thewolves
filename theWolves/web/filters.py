import django_filters
from .models import *
from django import forms

# Filter class for branch drill down. state & city variables fill the dropdown lists for filtering data.
class BranchFilter(django_filters.FilterSet):
# Initialise field variables
    state = django_filters.AllValuesFilter(field_name="state")
    city = django_filters.AllValuesFilter(field_name="city")
# Class meta attributes - configure model to use and which fields to include
    class Meta:
        model = Branch
		# Can be set to exclude filter fields or include filter fields.
        exclude = ['branchid','street','tellno']

# Filter class to display where vehicles are currently located.
class VehicleLocationFilter(django_filters.FilterSet):
    returnstore = django_filters.AllValuesFilter(field_name="returnstore")
# Class meta attributes - configure model to use and which fields to include
    class Meta:
        model = Orders
        fields = ['returnstore', 'rentedvehicle', ]


class DisplayBranchesDatabaseFilter(django_filters.FilterSet):
    state = django_filters.AllValuesMultipleFilter()
    class Meta:
        model = Branch
        fields=['state',]

class DisplayVehiclesDatabaseFilter(django_filters.FilterSet):
    pricenew = django_filters.RangeFilter()
    make = django_filters.CharFilter(lookup_expr='icontains')
    model = django_filters.CharFilter(lookup_expr='icontains')
    series =  django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.RangeFilter()
    enginesize = django_filters.AllValuesMultipleFilter()
    fuelsystem = django_filters.AllValuesMultipleFilter()
    tankcapacity = django_filters.AllValuesMultipleFilter()
    power = django_filters.AllValuesMultipleFilter()
    seatcapacity = django_filters.AllValuesMultipleFilter()
    standardtransmission = django_filters.AllValuesMultipleFilter()
    bodytype= django_filters.AllValuesMultipleFilter()
    drive= django_filters.AllValuesMultipleFilter()
    wheelbase= django_filters.AllValuesMultipleFilter()

    class Meta:
        model = Vehicles
        fields= ['make','model','series','year','pricenew','enginesize','fuelsystem','tankcapacity','power','seatcapacity','standardtransmission','bodytype','drive','wheelbase',]

class DisplaCustomersDatabaseFilter(django_filters.FilterSet):
    gender = django_filters.AllValuesMultipleFilter()
    occupation = django_filters.AllValuesMultipleFilter()

    class Meta:
        model = Customer
        fields= ['gender','occupation',]

class DisplaOrdersDatabaseFilter(django_filters.FilterSet):
    # orderid
    createdate = django_filters.DateFromToRangeFilter()
    pickupdate = django_filters.DateFromToRangeFilter()
    returndate =django_filters.DateFromToRangeFilter()
    pickupstore = django_filters.AllValuesMultipleFilter()
    returnstore = django_filters.AllValuesMultipleFilter()
    rentedvehicle = django_filters.AllValuesMultipleFilter()
    # customer =
    class Meta:
        model = Orders
        fields= ['createdate','pickupdate','returndate','pickupstore','returnstore','rentedvehicle',]

# Filter class to display vehicle status in a table.
class VehicleStatusFilter(django_filters.FilterSet):
    vehicleid = django_filters.AllValuesFilter(field_name="vehicleid")
    vehiclestatus = django_filters.AllValuesFilter(field_name="vehiclestatus")
    class Meta:
        model = Vehicles
        fields = ['vehicleid', 'make', 'model', 'series', 'year', 'vehiclestatus',]
