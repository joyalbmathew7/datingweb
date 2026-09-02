from django.urls import path

from locations.views import CityListView, CountryListView, StateListView

urlpatterns = [
    path("countries/", CountryListView.as_view(), name="countries"),
    path("states/", StateListView.as_view(), name="states"),
    path("cities/", CityListView.as_view(), name="cities"),
]
