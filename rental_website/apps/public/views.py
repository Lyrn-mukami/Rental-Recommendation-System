from django.shortcuts import render
from joblib import load

model = load('rental_website/SavedModel/model.joblib')

def index(request):
    return render(request, 'index.html')
def preferences(request):
    return render(request, 'preferences.html')
def critique(request):
    location = request.GET['location']
    bedrooms = request.GET['bedrooms']
    bathrooms = request.GET['bathrooms']
    price = request.GET['price']
    y_pred = model.predict([[location,bedrooms,bathrooms,price]])
    print(y_pred)

    return render(request, 'critiquing.html', {'cluster': y_pred})
def listings(request):
    return render(request, 'listings.html')
