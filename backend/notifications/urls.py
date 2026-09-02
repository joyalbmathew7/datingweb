from django.urls import path

from notifications.views import MarkNotificationsReadView, NotificationListView


urlpatterns = [
    path("", NotificationListView.as_view(), name="notifications"),
    path("read/", MarkNotificationsReadView.as_view(), name="mark-notifications-read"),
]
