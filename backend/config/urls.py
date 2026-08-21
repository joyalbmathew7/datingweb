from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/v1/auth/", include("accounts.urls")),
    path(
    "api/v1/profiles/",
    include("profiles.urls"),
),
path(
    "api/v1/discovery/",
    include("discovery.urls"),
),
path(
    "api/v1/interactions/",
    include("interactions.urls"),
),
path("api/v1/matches/", include("matches.urls")),
path("api/v1/chats/",include("chats.urls"))
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)