from django.contrib import admin

from .models import Country, State, City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code")
    search_fields = ("name",)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country")
    list_filter = ("country",)
    search_fields = ("name",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "state")
    list_filter = ("state",)
    search_fields = ("name",)