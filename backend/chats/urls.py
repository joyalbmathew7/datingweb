from django.urls import path

from chats.views import (
    MyConversationsView,
    ConversationMessagesView,
)


urlpatterns = [
    path(
        "",
        MyConversationsView.as_view(),
        name="my-conversations",
    ),
    path(
        "<uuid:uuid>/messages/",
        ConversationMessagesView.as_view(),
        name="conversation-messages",
    ),
]