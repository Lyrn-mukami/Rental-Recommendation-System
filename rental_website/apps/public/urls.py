from django.urls import path

from . import views

app_name="public"
urlpatterns = [
    path('', views.index, name="index"),
    path('preferences', views.preferences, name="preferences"),
    path('preferences/critique', views.critique, name="critique"),
    path('preferences/listings', views.listings, name="listings"),
    path('listing/<int:id>', views.listing, name="listing")
]