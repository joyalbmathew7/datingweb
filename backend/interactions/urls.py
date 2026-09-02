from django.urls import path

from interactions.views import InteractionView,MyMatchesView,BlockView,UnblockView,LikedMeView

urlpatterns = [
    path(
        "",
        InteractionView.as_view(),
        name="create-interaction",
    ),
    path(
        "matches/",
        MyMatchesView.as_view(),
        name="my-matches",
    ),
    path("block/", BlockView.as_view(),name="block-profile"),
    path("unblock/", UnblockView.as_view(), name="unblock-profile"),
    path("liked-me/", LikedMeView.as_view(), name = "liked-me")
]