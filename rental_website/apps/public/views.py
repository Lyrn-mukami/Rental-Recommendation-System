from django.shortcuts import render
from joblib import load
from django.http import JsonResponse
import json
import pandas as pd
from .recommend import Recommender
from rental_website.apps.employee.models import Property

def index(request):
    return render(request, 'index.html')
def preferences(request):
    return render(request, 'preferences.html')
def listings(request):
    choice = request.GET.getlist('choice')
    location = request.GET.getlist('location')
    bedrooms = request.GET.getlist('bedrooms')
    bathrooms = request.GET.getlist('bathrooms')
    price = request.GET.getlist('price')
    property = {'location':location, 'bedrooms':bathrooms, 'bathrooms':bathrooms, 'price':price, 'choice':choice}
    print(property)
    recommendations = Recommender().recommend(property)
    recommendations = recommendations.reset_index().to_json(orient ='records') 
    data = []
    data = json.loads(recommendations)
    return render(request, 'listings.html', {'recommendations':data})
def critique(request):
    location = request.GET['location']
    bedrooms = request.GET['bedrooms']
    bathrooms = request.GET['bathrooms']
    price = request.GET['price']
    property = {'location':[location], 'bedrooms':[bedrooms], 'bathrooms':[bathrooms], 'price':[price]}
    recommendations = Recommender.critique(property) 
    recommendations = recommendations.reset_index().to_json(orient ='records') 
    data = []
    data = json.loads(recommendations)            
    return render(request, 'critiquing.html',{'recommendations':data})
def list_view(request):
    properties = Property.objects.all()
    listing_df = pd.DataFrame.from_records(properties.values('location', 'bedrooms', 'bathrooms', 'price'))

    return render(request, 'listings.html', {'properties':listings})