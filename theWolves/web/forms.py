from django import forms

from .models import Branch,Vehicles,Customer
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.forms.widgets import SelectDateWidget
#Crispy forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import InlineField, FormActions, StrictButton, Div

# Form class : dropdown contains Australian States
class StateForm(forms.Form):
    #Get states available from Branch database
    statesAvailable = Branch.objects.values('state').distinct()
    states = [('Nationwide','--ALL--')]
    for state in statesAvailable:
        states.append((state['state'],state['state']))

    state = forms.ChoiceField(choices = states,label = "State")
    state.widget.attrs.update({'class':'form-control'})
    state.widget.attrs.update({'id':'state-top'})

#Form class for checkboxes filtering data displayed in recommendationresults.html
class FilterRecommendationResultsForm(forms.Form):
    def __init__(self,*args,**kwargs):
        vehicles = kwargs.pop("cars")
        super(FilterRecommendationResultsForm, self).__init__(*args,**kwargs)

        #Get locations of the results
        locationsWithDuplicate = []
        # Get seat capacities of the results
        seatWithDuplicate = []
        for v in vehicles:
            locationsWithDuplicate.append((v.latest_order().returnstore,v.latest_order().returnstore))
            seatWithDuplicate.append(v.seatcapacity)

        #locations without duplicates
        locations = [('----','----')]
        for l in locationsWithDuplicate:
            if l not in locations:
                locations.append((l[0],l[0]))

        print(locations)


        #seatcapacity without duplicates
        seat = [('----','----')]
        for s in seatWithDuplicate:
            if (s,s) not in seat:
                seat.append((s,s))
        print(seat)

        self.fields['location'] = forms.ChoiceField(choices = locations)

        self.fields['location'].widget.attrs.update({'class':'form-control'})
        self.fields['location'].widget.attrs.update({'id':'location-queries'})


        self.fields['seat'] = forms.ChoiceField(choices = seat)

        self.fields['seat'].widget.attrs.update({'class':'form-control'})
        self.fields['seat'].widget.attrs.update({'id':'seat-queries'})


dob = forms.DateField(required=False,
                       widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),years=range(1980, 2012)))
# Form class for creating a new customer record
class addCustomerForm(forms.ModelForm):
# Create a widget to display the date of birth as a date picker in the form
    dob = forms.DateField(required=False,
                           widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),years=range(1940, 2012)))
    class Meta:
        model = Customer
        fields = ['customerid','fname','lname', 'telno','address','dob','gender','occupation']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save customer'))
