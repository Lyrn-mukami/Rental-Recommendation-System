from django.shortcuts import render
import pandas as pd
import json

from .recommend import Recommender
from rental_website.apps.employee.models import Property, Location
from .forms import LocationForm

def index(request):
    return render(request, 'index.html')
def preferences(request): #get the location listings from the DB display to user for selection
    locations = Location.objects.all()
    return render(request, 'preferences.html', {'locations':locations})
def critique(request):
    location = request.GET['location']
    bedrooms = request.GET['bedrooms']
    bathrooms = request.GET['bathrooms']
    price = request.GET['price']
    property = {'location':[location], 'bedrooms':[bedrooms], 'bathrooms':[bathrooms], 'price':[price]}
    recommendations = Recommender.recommend(property) 
    recommendations = recommendations.reset_index().to_json(orient ='records') 
    data = []
    data = json.loads(recommendations)            
    return render(request, 'critiquing.html',{'recommendations':data})
def listings(request):
    choice = request.GET.getlist('choice')
    location = request.GET.getlist('location')
    bedrooms = request.GET.getlist('bedrooms')
    bathrooms = request.GET.getlist('bathrooms')
    price = request.GET.getlist('price')
    property = {'location':location, 'bedrooms':bedrooms, 'bathrooms':bathrooms, 'price':price, 'choice':choice}
    print(property)
    recommendations = Recommender.recommend(property)
    recommendations = pd.concat(recommendations, ignore_index=False)
    recommendations = recommendations.reset_index(drop=True).to_json(orient='records')
    recommendations = json.loads(recommendations)
    return render(request, 'listings.html', {'recommendations':recommendations})
def listing(request, id=0):
    property = Property.objects.get(pk=id)
    return render(request, 'individuallisting.html', {'property':property} )