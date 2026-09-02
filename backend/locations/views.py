from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from locations.models import City, Country, State
from locations.serializers import CitySerializer, CountrySerializer, StateSerializer


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all().order_by("name")
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class StateListView(generics.ListAPIView):
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        queryset = State.objects.all().order_by("name")
        country_id = self.request.query_params.get("country")
        if country_id:
            queryset = queryset.filter(country_id=country_id)
        return queryset


class CityListView(generics.ListAPIView):
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        queryset = City.objects.all().order_by("name")
        state_id = self.request.query_params.get("state")
        if state_id:
            queryset = queryset.filter(state_id=state_id)
        return queryset
