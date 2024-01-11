from django.urls import path

from . import views

app_name="employee"
urlpatterns = [
    path('dashboard', views.index, name="dashboard"),
    path('property/listings', views.viewProperty, name="listings"),
    path('property/new', views.addProperty, name="newProperty"),
    path('property/edit<int:id>', views.editProperty, name="editProperty"),
    path('property/delete<int:id>', views.deleteProperty, name="deleteProperty"),
]