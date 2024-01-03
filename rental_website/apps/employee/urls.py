from django.urls import path

from . import views

app_name="employee"
urlpatterns = [
    path('dashboard', views.index, name="dashboard"),
]