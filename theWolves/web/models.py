# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)



class Branch(models.Model):
    branchid = models.IntegerField(db_column='branchID', primary_key=True)  # Field name made lowercase.
    city = models.CharField(max_length=45, blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    street = models.CharField(max_length=45, blank=True, null=True)
    tellno = models.CharField(db_column='tellNo', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'branch'

    def __str__(self):
        return self.city

    def get_absolute_url(self):
        return "/corporate/branches/%i/" % self.branchid


class Customer(models.Model):
    customerid = models.IntegerField(db_column='customerID', primary_key=True)  # Field name made lowercase.
    fname = models.CharField(verbose_name='First Name',db_column='fName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    lname = models.CharField(verbose_name='Last Name',db_column='lName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    telno = models.CharField(db_column='telNo', max_length=45, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(max_length=45, blank=True, null=True)
    dob = models.DateField(db_column='DOB', blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=45, blank=True, null=True)
    occupation = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'

    def __str__(self):
        return self.fname+' '+self.lname


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Orders(models.Model):
    orderid = models.AutoField(db_column='orderID', primary_key=True)  # Field name made lowercase.
    createdate = models.DateField(db_column='createDate', blank=True, null=True)  # Field name made lowercase.
    pickupdate = models.DateField(db_column='pickupDate', blank=True, null=True)  # Field name made lowercase.
    returndate = models.DateField(db_column='returnDate', blank=True, null=True)  # Field name made lowercase.
    pickupstore = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column='pickupStore', blank=True, null=True,related_name = 'pickupstorefk')  # Field name made lowercase.
    returnstore = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column='returnStore',verbose_name='Current Location', blank=True, null=True,related_name = 'returnstorefk')  # Field name made lowercase.
    rentedvehicle = models.ForeignKey('Vehicles', models.DO_NOTHING, db_column='rentedVehicle', blank=True, null=True)  # Field name made lowercase.
    customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customer', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'

    def __str__(self):
        return 'Order ' + str(self.orderid)



class Vehicles(models.Model):
    RETURNED = 'R'
    NOTRETURNED = 'NR'
    VEHICLE_STATUS_CHOICES = (
		('R', 'Returned'),
        ('NR', 'Not Returned'),
		)
    vehicleid = models.IntegerField(db_column='vehicleID', primary_key=True)  # Field name made lowercase.
    make = models.CharField(max_length=45, blank=True, null=True)
    model = models.CharField(max_length=45, blank=True, null=True)
    series = models.CharField(max_length=45, blank=True, null=True)
    year = models.TextField(blank=True, null=True)  # This field type is a guess.
    pricenew = models.IntegerField(db_column='priceNew',verbose_name='Price $', blank=True, null=True)  # Field name made lowercase.
    enginesize = models.CharField(db_column='engineSize', max_length=45, blank=True, null=True)  # Field name made lowercase.
    fuelsystem = models.CharField(db_column='fuelSystem', max_length=45, blank=True, null=True)  # Field name made lowercase.
    tankcapacity = models.CharField(db_column='tankCapacity', max_length=45, blank=True, null=True)  # Field name made lowercase.
    power = models.CharField(max_length=45, blank=True, null=True)
    seatcapacity = models.IntegerField(db_column='seatCapacity', blank=True, null=True)  # Field name made lowercase.
    standardtransmission = models.CharField(db_column='standardTransmission', max_length=45, blank=True, null=True)  # Field name made lowercase.
    bodytype = models.CharField(db_column='bodyType', max_length=45, blank=True, null=True)  # Field name made lowercase.
    drive = models.CharField(max_length=45, blank=True, null=True)
    wheelbase = models.CharField(max_length=45, blank=True, null=True)
    vehiclestatus = models.CharField(max_length = 2, choices = VEHICLE_STATUS_CHOICES, default = 'NOTRETURNED')

    class Meta:
        managed = False
        db_table = 'vehicles'
        ordering = ('make',)

    def __str__(self):
        return self.make+' '+self.model+' '+self.series

    def latest_order(self):
        return self.orders_set.latest('returndate')

    def get_absolute_url(self):
        return "/corporate/vehicles/%i/" % self.vehicleid
