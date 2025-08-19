from django import forms
from rental_website.apps.employee.models import Location

class LocationForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset = Location.objects.all(),
        empty_label= "Select a location"
    )