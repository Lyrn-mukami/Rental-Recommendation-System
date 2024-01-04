from django.urls import path

from . import views

app_name="employee"
urlpatterns = [
    path('dashboard', views.index, name="dashboard"),
    path('listings', views.viewProperty, name="listings"),
    path('newProperty', views.addProperty, name="newProperty"),
    path('editProperty', views.editProperty, name="editProperty"),
    path('deleteProperty', views.deleteProperty, name="deleteProperty"),
]