from django.contrib import admin
from .models import Orders
from .models import Vehicles
from .models import Customer
from .models import Branch

# Register your models here.
admin.site.register(Orders)
admin.site.register(Vehicles)
admin.site.register(Customer)
admin.site.register(Branch)
