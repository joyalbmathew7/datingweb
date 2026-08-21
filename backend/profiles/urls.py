from django.urls import path

# from .views import CreateProfileView
from profiles.views import CreateProfileView,MyProfileView,UpdateProfileView,UploadPhotoView,DeletePhotoView,SetProfilePictureView,DiscoverProfilesView

urlpatterns = [
    path(
        "",
        CreateProfileView.as_view(),
        name="create-profile",
        
    ),
    # path(
    # "me/",
    # MyProfileView.as_view(),
    # name="my-profile",
    # ),
    path("me/", MyProfileView.as_view(), name="my-profile"),
    path(
    "me/update/",
    UpdateProfileView.as_view(),
    name="update-profile",
    ),
    path(
    "photos/",
    UploadPhotoView.as_view(),
    name="upload-photo",
    ),
    path(
    "photos/<uuid:pk>/",
    DeletePhotoView.as_view(),
    name="delete-photo",
),
path(
    "photos/<uuid:pk>/profile-picture/",
    SetProfilePictureView.as_view(),
    name="set-profile-picture",
),
path("discover/",DiscoverProfilesView.as_view(),name="discover-profiles")
]