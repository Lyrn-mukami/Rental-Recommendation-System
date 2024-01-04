from django.shortcuts import render

def index(request):
    return render(request, 'employee/dashboard.html')

def viewProperty(request):
     return render(request, 'employee/viewProperty.html')

def addProperty(request):
    return render(request, 'employee/addProperty.html')

def editProperty(request):
     return render(request, 'employee/editProperty.html')
     
def deleteProperty(request):
     return render(request, 'employee/viewProperty.html')
