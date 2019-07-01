# Django filters
import django_filters
from django_filters.views import FilterView
from .filters import *

# Django views
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django_tables2 import SingleTableView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.views.generic.edit import UpdateView
# Django Forms
from .forms import *

# Django Models Function
from django.db.models import Count,F,Max,Q
from django.db.models.functions import TruncMonth

# Models of the Database
from .models import Vehicles
from .models import Orders
from .models import Branch
from .models import Customer

# Django tables
from django_tables2 import RequestConfig
from django_tables2.views import SingleTableMixin, MultiTableMixin
from .tables import *

# Django core modules
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


# Authentication
from django.contrib.auth.decorators import login_required


from django.contrib.auth.decorators import user_passes_test

from .decorators import group_required
from django.utils.decorators import method_decorator

from django.shortcuts import redirect


###############################################################
##CORPORATE View
######################################################
@group_required('Corporate')
def corp_dashboard(request):
    orders = Orders.objects.all()
    # Get total orders
    totalOrders = Orders.objects.all().count()
    return render(request,'web/corporate/corp_dashboard.html',{'orders':orders,'totalOrders':totalOrders})

@group_required('Corporate')
def branches_reports(request):

    return render(request,'web/branches_reports.html',{})

@group_required('Corporate')
def vehicles_reports(request):

    return render(request,'web/vehicles_reports.html',{})

@group_required('Corporate')
def customers_reports(request):
    gender = Customer.objects.all().annotate(num=Count('gender')).values('gender')                  #gender radio
    occupation = Customer.objects.all().annotate(num=Count('occupation')).values('occupation')      #occupation radio
    return render(request,'web/customers_reports.html',{'gender':gender, 'occuaption':occupation})

@group_required('Corporate')
def vehicle_performance(request):
    vehicles = Vehicles.objects.all().values('bodytype').distinct().order_by('bodytype')
    print(vehicles)
    return render(request,'web/corporate/vehicle_performance/vehicle_performance.html',{'vehicles':vehicles})

@group_required('Corporate')
def vehicle_performance_result(request):
    date = str(request.GET['date'])
    year = int(date[0:4])
    month = int(date[5:7])
    v = request.GET.getlist('checks[]')

    if not v:
        categories = Orders.objects.all().select_related('rentedvehicle')
        categories = categories.values('rentedvehicle__bodytype').filter(pickupdate__year = year, pickupdate__month = month)
        categories = categories.annotate(num=Count('rentedvehicle__bodytype')).order_by('-num').distinct()
    else:
        categories = Orders.objects.all().select_related('rentedvehicle')
        categories = categories.values('rentedvehicle__bodytype').filter(pickupdate__year = year, pickupdate__month = month)
        categories = categories.filter(rentedvehicle__bodytype__in=v)
        categories = categories.annotate(num=Count('rentedvehicle__bodytype')).order_by('-num').distinct()

    # convert categories to list
    categoriesWithOrder = list(categories)

    # Create a list to get the name of categories (bodytypes)
    categoriesWithOrder2 = []
    for c in categoriesWithOrder:
        categoriesWithOrder2.append(c['rentedvehicle__bodytype'])

    # If category in v is not in categoriesWithOrder2, add the category with num equals 0
    for c in v:
        if c not in categoriesWithOrder2:
            categoriesWithOrder.append({'rentedvehicle__bodytype':c,'num':0})
    return render(request,'web/corporate/vehicle_performance/vehicle_performance_result.html',{'categories':categoriesWithOrder})

# Display Branches Data from the Database
@group_required('Corporate')
def display_branches_database(request):
    branches = Branch.objects.all();
    branches_filter = DisplayBranchesDatabaseFilter(request.GET,queryset = branches)
    return render(request,'web/corporate/display_database/display_branches_database.html',{'branches_filter':branches_filter})

# Display Vehicles Data from the Database
@group_required('Corporate')
def display_vehicles_database(request):
    vehicles = Vehicles.objects.all();
    vehicles_filter = DisplayVehiclesDatabaseFilter(request.GET,queryset = vehicles)
    return render(request,'web/corporate/display_database/display_vehicles_database.html',{'vehicles_filter':vehicles_filter})

# Display Customers Data from the Database
@group_required('Corporate')
def display_customers_database(request):
    customers = Customer.objects.all();
    customers_filter = DisplaCustomersDatabaseFilter(request.GET,queryset = customers)
    return render(request,'web/corporate/display_database/display_customers_database.html',{'customers_filter':customers_filter})

# Display Orders Data from the Database
@group_required('Corporate')
def display_orders_database(request):
    orders =Orders.objects.all();
    orders_filter = DisplaOrdersDatabaseFilter(request.GET,queryset = orders)
    return render(request,'web/corporate/display_database/display_orders_database.html',{'orders_filter':orders_filter})



###############################################################
##CORPORATE View END
######################################################



###############################################################
##STAFF View
######################################################
@group_required('Staff')
def staff_dashboard(request):
    return render(request,'web/staff/staff_dashboard.html',{})

# Class based view for creating a new customer record in the database
@method_decorator([login_required, group_required('Staff')], name='dispatch')
class addCustomerView(CreateView):
    template_name = "web/staff/addCustomer.html"
    form_class = addCustomerForm
    model = Customer
# Define a function for updating the view upon form submission
    def get_success_url(self):
        return reverse('addCustomer')

# Class based view for generating a filtered table showing vehicle status
@method_decorator([login_required, group_required('Staff')], name='dispatch')
class UpdateVehicleStatusView(SingleTableMixin, FilterView):
    table_class = VehicleStatus
    model = Vehicles
    template_name = 'web/staff/vehicle_status/updateVehicleStatus.html'
    filterset_class = VehicleStatusFilter

# Class based view for CRUD operation
@method_decorator([login_required, group_required('Staff')], name='dispatch')
class StatusUpdate(UpdateView):
    model = Vehicles
    fields = ['vehiclestatus']
    template_name = 'web/staff/vehicle_status/vehicleStatusDetail.html'

###############################################################
##STAFF View END
######################################################

# View for homepage
def homepage(request):
    # Drop down form with list of Australian states
    stateForm = StateForm()

    topCars = Vehicles.objects.annotate(num =Count('orders'))
    topCars = topCars.order_by('-num').annotate(max_date=Max('orders__returndate'))
    topCars = topCars.filter(orders__returndate=F('max_date'))[:20]
    return render(request,'web/homepage/homepage.html',{'stateForm':stateForm,'topCars':topCars})

#View for Ajax displaying top cars on the homepage
def displayTopCars(request):
    if request.GET['state'] == 'Nationwide':
        topCars = Vehicles.objects.annotate(num =Count('orders'))
        topCars = topCars.order_by('-num').annotate(max_date=Max('orders__returndate'))
        topCars = topCars.filter(orders__returndate=F('max_date'))[:20]
    else:
        topCars = Vehicles.objects.annotate(num =Count('orders'))
        topCars = topCars.order_by('-num').annotate(max_date=Max('orders__returndate'))
        topCars = topCars.filter(orders__returndate=F('max_date'), orders__returnstore__state = request.GET['state'])[:20]


    return render(request, 'web/homepage/display_top_cars.html',{'topCars':topCars,'state':request.GET['state']})

#View for displaying specification of each car
def specification(request, vehicleid):
    car = Vehicles.objects.get(pk=vehicleid)
    return render(request,'web/each_car_specification/specification.html',{'car':car})

#View displaying states to choose which state to display the top cars
def recommendation(request):
    # Drop down form with list of Australian states
    stateForm = StateForm()

    return render(request,'web/recommendation/recommendation.html',{'stateForm':stateForm})

# View for Search Cars Result Page (Recommendation Results)
def recommendationResults(request):
    # any state
    if request.POST['state'] == 'Nationwide':
        cars = Vehicles.objects.annotate(max_date=Max('orders__returndate'))
        cars = cars.filter(orders__returndate=F('max_date'))
    # particular state
    else:
        cars = Vehicles.objects.annotate(max_date=Max('orders__returndate'))
        cars = cars.filter(orders__returndate=F('max_date'),orders__returnstore__state = request.POST['state'])

    filterForm = FilterRecommendationResultsForm(cars= cars)
    return render(request,'web/recommendation/recommendationresults.html',{'cars':cars,'state':request.POST['state'],'filterForm':filterForm})


#View ajax page for sorting recommendation results based on
# branch location selected on recommendationresults page
def sort_location(request):
    location = request.GET['location']
    seat = request.GET['seat']
    firstLocation = request.GET['findState']

    state = Vehicles.objects.filter(orders__returnstore__city = firstLocation)
    state = state.values('orders__returnstore__state').distinct()[0]['orders__returnstore__state']

    # all branches in state
    if location == '----':
        vehicles = Vehicles.objects.annotate(max_date=Max('orders__returndate'))
        vehicles = vehicles.filter(orders__returndate=F('max_date'),orders__returnstore__state = state)
    # particular branch
    else:
        vehicles = Vehicles.objects.annotate(max_date=Max('orders__returndate'))
        vehicles = vehicles.filter(orders__returndate=F('max_date'),orders__returnstore__city = location)

    if seat != '----':
        vehicles = vehicles.filter(seatcapacity= request.GET['seat'])

    return render(request,'web/recommendation/sort_location.html',{'vehicles':vehicles})







# Display store locations
def branch_store_location(request):
    branch_store_location= Branch.objects.all()
    return render(request,'web/store_locator/branch_store_location.html',{'branch_store_location':branch_store_location})


#Display vehicles available in any particular branch
def vehicles_in_branch(request,branchName):
    vehicles = Vehicles.objects.annotate(max_date=Max('orders__returndate'))
    vehicles = vehicles.filter(orders__returndate=F('max_date'),orders__returnstore__city = branchName)
    return render(request,'web/vehicles_in_branch/vehicles_in_branch.html',{'vehicles':vehicles,'branchName':branchName,})

# Redirect destination after login
def login_success(request):
    # Redirects users based on whether they are in the admins group
    if request.user.groups.filter(name="Corporate").exists():
        # user is a corporate employee
        return redirect("corp_dashboard")
    else:
        # Change it to staff page later
        return redirect("staff_dashboard")



def load_branch_name(request):
    if(request.GET['branch'] == '----'):
        print('test')
        return render(request, 'web/load_branch_name.html', {})
    else :
        branch = request.GET
        return render(request, 'web/load_branch_name.html', {'branch':branch})


def load_branches(request):
    state = request.GET['state']
    branch = Branch.objects.filter(state = state)
    return render(request,'web/load_branches.html',{'branch':branch})

def branchDashboard(request):
    stateAndBranchForm = StateAndBranchForm();
    return render(request,'web/branchdashboard.html',{'stateAndBranchForm':stateAndBranchForm})

def companyDashboard(request):
    return render(request,'web/companydashboard.html',{})

def specification(request, vehicleid):
    car = Vehicles.objects.get(pk=vehicleid)
    return render(request,'web/each_car_specification/specification.html',{'car':car})


# Listview based class for showing top 10 cars on the corporate home page
class CorpHomeView(ListView):
    template_name = 'web/corphomepage.html'
    model = Orders
    context_object_name = 'mostPopularVehicles'
    queryset = Orders.objects.annotate(Count('rentedvehicle')).order_by('-rentedvehicle__count')[:10]

# Filter view of the branches used in 'branchdrilldown.html.
class FilteredBranchListView(SingleTableMixin, FilterView):
    table_class = BranchTable
    model = Branch
    template_name = 'web/corporate/branchDrillDown.html'
    filterset_class = BranchFilter

# Filter view to show all vehicles at all branches or a filtered branch selection
class FilteredVehicleLocationView(SingleTableMixin, FilterView):
    table_class = VehicleLocation
    model = Orders
    fields = ['returnstore', 'rentedvehicle',]
    template_name = 'web/corporate/branchDrillDownDetail.html'
    filterset_class = VehicleLocationFilter





# Class based view for customer statistics
class CustomerInfo(MultiTableMixin, TemplateView):
    model = Customer
    template_name = 'web/corporate/customerStats.html'
    qs = Customer.objects.all()
# Generate a function to count total customers and pass the query to the template view
    def customer_count(self):
        case = Customer.objects.all().count()
        return case
# Generate a function to count distinct occupations and pass the query to the template view
    def occupation_count(self):
        case1 = Customer.objects.values('occupation').distinct().count()
        return case1
# Generate a table to display all customers - functionality allows for multiple tables if required.
    tables = [
        CustomerTable(qs),
#        CustomerTable(qs, exclude=('customerid','address','dob','gender','occupation' ))
    ]
# Display 10 results per page of the table
    table_pagination = {
        'per_page': 10
    }

def comparisonbranch(request):
    branchs = Branch.objects.all().order_by('city')
    return render(request, 'web/corporate/branch_comparison/comparisonbranch.html', {'branchs':branchs})

# Comparison branch result
def branchcomparison(request):
    date = str(request.GET['date'])
    year = int(date[0:4])
    month = int(date[5:7])
    b = request.GET.getlist('checks[]')

    if not b:
        branchs = Orders.objects.all().select_related('pickupstore').values('pickupstore__city').filter(pickupdate__year = year, pickupdate__month = month).annotate(num=Count('pickupstore__city')).order_by('pickupstore__city')
        branchs = branchs.values('pickupstore__city').filter(pickupdate__year = year, pickupdate__month = month)
        branchs = branchs.annotate(num=Count('pickupstore__city')).order_by('pickupstore__city')
    else:
        branchs = Orders.objects.all().select_related('pickupstore')
        branchs = branchs.values('pickupstore__city').filter(pickupdate__year = year, pickupdate__month = month)
        branchs = branchs.filter(pickupstore__city__in=b).annotate(num=Count('pickupstore__city')).order_by('pickupstore__city')

    # Convert branchs to list
    branchsWithOrder = list(branchs)

    # Create a list to get the name of the store in branchs
    branchsWithOrder2 = []
    for s in branchsWithOrder:
        branchsWithOrder2.append(s['pickupstore__city'])

    # If branch in b is not in branchs,add the branch with num equals 0
    for s in b:
        if s not in branchsWithOrder2:
            branchsWithOrder.append({'pickupstore__city':s,'num':0})

    return render(request, 'web/corporate/branch_comparison/branchcomparison.html', {'branchs':branchsWithOrder})



def view_all_vehicles(request):
    cars= Vehicles.objects.annotate(max_date=Max('orders__returndate'))
    cars= cars.filter(orders__returndate=F('max_date'))
    return render(request,'web/view_all_vehicles.html',{'cars':cars})



def list_all_branches(request):
    branches = Branch.objects.all()
    return render(request,'web/list_all_branches.html',{'branches':branches})


def salesTrend(request,branchid):
    branch = Branch.objects.get(pk = branchid)
    salesDataMonthly = Orders.objects.annotate(month=TruncMonth('pickupdate')).values('month').annotate(pickup=Count('orderid',filter=Q(pickupstore = branch),distinct = True)).annotate(returned=Count('orderid',filter=Q(returnstore= branch),distinct = True))

    return render(request,'web/salestrend.html',{'salesDataMonthly':salesDataMonthly})



def view_parking_lot(request):
    parking_lot= Vehicles.objects.annotate(max_date=Max('orders__returndate'))
    parking_lot= parking_lot.filter(orders__returndate=F('max_date'), orders__returnstore__city = 'brisbane').count()
    space = 4000 - (parking_lot * 17)
    return render(request,'web/parking_lot_availability.html',{'parking_lot':parking_lot, 'space':space})

def view_top_customer_rentals(request):
    top_customer_rentals= Orders.objects.filter(customer__customerid = 11010)[0].rentedvehicle
    return render(request, 'web/view_top_customer_rentals.html', {'top_customer_rentals':top_customer_rentals})
