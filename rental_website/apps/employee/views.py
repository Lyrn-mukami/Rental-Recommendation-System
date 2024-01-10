from django.shortcuts import render, redirect
from .models import Location, Property
from .forms import PropertyForm
def index(request):
     property = Property.objects.all()
     return render(request, 'employee/dashboard.html', {'property': property})

def viewProperty(request):
     property = Property.objects.all()
     return render(request, 'employee/viewProperty.html', {'property': property})

def addProperty(request):
     if request.method == 'GET':
          form = PropertyForm()
          return render(request, 'employee/addProperty.html', {'form': form})
     else:
        form = PropertyForm(request.POST) 
        if form.is_valid():
          form.save()
     return redirect ('/staff/listings')


def editProperty(request, id=0):
     if request.method == "GET":
          property = Property.objects.get(pk=id)
          form = PropertyForm(instance=property)
          return render(request, 'employee:editProperty.html', {'form': form})
     else:
          property = Property.objects.get(pk=id)
          form = PropertyForm(request.POST, instance=property) 
          if form.is_valid():
               form.save()
          return redirect ('employee:listings')
def deleteProperty(request, id=0):
     property = Property.objects.get(pk=id)
     property.delete()
     return redirect ('employee:listings')
