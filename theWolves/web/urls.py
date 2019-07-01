from django.urls import path, re_path,include
from django.conf.urls import url
from . import views
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .filters import *

from django.contrib.auth.views import LoginView

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.homepage,name = 'homepage'),
    path('display_top_cars/', views.displayTopCars, name='ajax_displayTopCars'),

    path('specification/<int:vehicleid>/', views.specification, name = 'specification'),

    path('recommendation/',views.recommendation,name = 'recommendation'),
    path('recommendationresults/',views.recommendationResults,name = 'recommendationResults'),
    path('sort-location/', views.sort_location, name='ajax_sort_location'),

    path('branch_store_location/', views.branch_store_location, name = 'branchstorelocation'),

    path('vehicles_in_branch/<str:branchName>/', views.vehicles_in_branch, name='vehicles_in_branch'),

    path('accounts/',include('django.contrib.auth.urls')),
    path(r'^login/',auth_views.LoginView.as_view(redirect_authenticated_user=True),name='login'),

    path('corp_dashboard/', views.corp_dashboard, name='corp_dashboard'),

	path('customers_reports/', views.customers_reports, name='customers_reports'),

    path('display_branches_database/', views.display_branches_database, name='display_branches_database'),

    path('display_vehicles_database/', views.display_vehicles_database, name='display_vehicles_database'),

    path('display_customers_database/', views.display_customers_database, name='display_customers_database'),

    path('display_orders_database/', views.display_orders_database, name='display_orders_database'),



    path('login_success/', views.login_success, name='login_success'),

    path('comparisonbranch/', views.comparisonbranch, name = 'comparisonbranch'),
    path('branchcomparison/',views.branchcomparison, name = 'branchcomparison'),


	path('vehicle_performance', views.vehicle_performance, name='vehicle_performance'),
	path('vehicle_performance_result', views.vehicle_performance_result, name='vehicle_performance_result'),

    path('staff_dashboard', views.staff_dashboard, name='staff_dashboard'),



    path('corporate/',views.CorpHomeView.as_view(), name = "corphomepage"),
	path('corporate/branches/', views.FilteredBranchListView.as_view(), name ='branchDrillDown'),
	path('corporate/branches/<int:pk>/', views.FilteredVehicleLocationView.as_view(), name = 'branchDrillDownDetail'),
	path('corporate/addCustomer/', views.addCustomerView.as_view(), name="addCustomer"),
	path('corporate/updateVehicleStatus/', views.UpdateVehicleStatusView.as_view(), name = 'updateVehicleStatus'),
	path('corporate/vehicles/<int:pk>/', views.StatusUpdate.as_view(), name='vehiclesDetailView'),
	path('corporate/customer/', views.CustomerInfo.as_view(), name='customerStats'),



    path('branchdashboard/',views.branchDashboard, name = 'branchDashboard'),
    path('companydashboard/',views.companyDashboard, name = 'companyDashboard'),

    path('salestrend/<int:branchid>',views.salesTrend, name = 'salestrend'),


    path('load_branches/', views.load_branches, name='ajax_load_branches'),
    path('load_branch_name/', views.load_branch_name, name='ajax_load_branch_name'),

    path('view_all_vehicles/', views.view_all_vehicles, name = 'viewallvehicles'),

    path('list_all_branches/',views.list_all_branches, name = 'list_all_branches'),


    path('view_parking_lot/', views.view_parking_lot, name = 'parkinglotavailability'),
    path('view_top_customer_rentals/', views.view_top_customer_rentals, name = 'viewtopcustomerrentals')


	]
