# Generated manually for the notifications feature.
import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("profiles", "0001_initial"),
        ("chats", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("notification_type", models.CharField(choices=[("LIKE", "Like"), ("MATCH", "Match"), ("MESSAGE", "Message")], max_length=12)),
                ("is_read", models.BooleanField(default=False)),
                ("actor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notifications_sent", to="profiles.profile")),
                ("conversation", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to="chats.conversation")),
                ("recipient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to="profiles.profile")),
            ],
            options={"ordering": ("-created_at",)},
        ),
    ]
