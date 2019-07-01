import django_tables2 as tables
from django_tables2.utils import A
from .models import *
import itertools

# Table class for generating filtered view of branches. Used by BranchFilter filter class.
class BranchTable(tables.Table):
# Initialise field, linkify attribute allows data in rows to be converted to URL
    city = tables.Column(linkify=True) 
    class Meta:
        model = Branch
        

# Table class for generating filtered view of branches. Used by VehicleLocationFilter filter class.
class VehicleLocation(tables.Table):
# Class meta attributes - configure model to use and which fields to include
	class Meta:
		model = Orders
		fields = ['returnstore','rentedvehicle',]

# Table class for generating a table used in displaying and updating vehicle status.
class VehicleStatus(tables.Table):
# Initialise field, linkify attribute allows data in rows to be converted to URL
    vehicleid = tables.Column(linkify=True)
# Class meta attributes - configure model to use and which fields to include
    class Meta:
        model = Vehicles

# Table class used to display all customer information
class CustomerTable(tables.Table):
	class Meta:
		model = Customer
