from django.shortcuts import render, redirect
from .models import Location, Property
from .forms import PropertyForm
from django.core.paginator import Paginator
def index(request):
     property = Property.objects.all()
     return render(request, 'employee/dashboard.html', {'property': property})

def viewProperty(request, page_number=1):
     property = Property.objects.all()
     paginator = Paginator(property,30)
     page_number = request.GET.get("page")
     page_obj = paginator.get_page(page_number)
     return render(request, 'employee/viewProperty.html', {'page_obj': page_obj})

def addProperty(request):
     if request.method == 'GET':
          form = PropertyForm()
          return render(request, 'employee/addProperty.html', {'form': form})
     else:
        form = PropertyForm(request.POST) 
        if form.is_valid():
          form.save()
     return redirect ('employee:listings')


def editProperty(request, id=0):
     if request.method == "GET":
          property = Property.objects.get(pk=id)
          form = PropertyForm(instance=property)
          return render(request, 'employee/editProperty.html', {'form': form})
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
