from django.shortcuts import render
from joblib import load
from django.http import JsonResponse
import json
import pandas as pd
from .recommend import Recommender

def index(request):
    return render(request, 'index.html')
def preferences(request):
    return render(request, 'preferences.html')
def listings(request):
    location = request.GET['location']
    bedrooms = request.GET['bedrooms']
    bathrooms = request.GET['bathrooms']
    price = request.GET['price']
    property = {'location':[location], 'bedrooms':[bathrooms], 'bathrooms':[bathrooms], 'price':[price]}
    recommendations = Recommender.recommend(property)
    recommendations = recommendations.reset_index().to_json(orient ='records') 
    data = []
    data = json.loads(recommendations)
    
    # return JsonResponse(recommendations)
    return render(request, 'listings.html',{'rec':data})
def critique(request):
    if request.method == 'POST':
        choice = request.GET['choice']
        return choice
    
    return render(request, 'critiquing.html')
