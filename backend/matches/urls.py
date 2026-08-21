from django.urls import path

from matches.views import MyMatchesView


urlpatterns = [
    path(
        "",
        MyMatchesView.as_view(),
        name="my-matches",
    ),
]