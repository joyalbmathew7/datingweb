from django.urls import path

from discovery.views import DiscoveryView


urlpatterns = [
    path(
        "",
        DiscoveryView.as_view(),
        name="discovery",
    ),
]