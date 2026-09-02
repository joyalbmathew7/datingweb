from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from profiles.services.profile import ProfileService


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=ProfileService.get_my_profile(self.request.user)
        ).select_related("actor", "conversation")


class MarkNotificationsReadView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        profile = ProfileService.get_my_profile(request.user)
        notifications = Notification.objects.filter(recipient=profile, is_read=False)
        notification_uuid = request.data.get("uuid")
        if notification_uuid:
            notifications = notifications.filter(uuid=notification_uuid)
        updated = notifications.update(is_read=True)
        return Response({"updated": updated}, status=status.HTTP_200_OK)
