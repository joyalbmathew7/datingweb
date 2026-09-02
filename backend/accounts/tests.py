from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.models import EmailOTP
from accounts.serializers import UserRegisterSerializer
from accounts.services.otp import OTPService

User = get_user_model()


class AuthFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_email_verification_sets_user_flag(self):
        user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="StrongPass123!",
        )

        otp = "123456"
        EmailOTP.objects.create(
            user=user,
            otp_hash=OTPService._hash_otp(otp),
            purpose=EmailOTP.Purpose.EMAIL_VERIFICATION,
            expires_at=timezone.now() + timedelta(minutes=5),
        )

        response = self.client.post(
            reverse("verify-email"),
            {"email": "alice@example.com", "otp": otp},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.email_verified)

    def test_registration_rejects_duplicate_email_case_insensitive(self):
        User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="StrongPass123!",
        )

        serializer = UserRegisterSerializer(
            data={
                "username": "bob",
                "email": "ALICE@example.com",
                "password": "StrongPass123!",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_password_reset_otp_flow_keeps_email_verification_separate(self):
        user = User.objects.create_user(
            username="charlie",
            email="charlie@example.com",
            password="StrongPass123!",
        )

        otp = "654321"
        EmailOTP.objects.create(
            user=user,
            otp_hash=OTPService._hash_otp(otp),
            purpose=EmailOTP.Purpose.PASSWORD_RESET,
            expires_at=timezone.now() + timedelta(minutes=5),
        )

        self.assertTrue(
            OTPService.verify_email_otp(
                user=user,
                otp=otp,
                purpose=EmailOTP.Purpose.PASSWORD_RESET,
            )
        )

        reset_token = OTPService.create_password_reset_token(user)
        self.assertIsNotNone(
            OTPService.verify_password_reset_token(user, reset_token)
        )

        user.refresh_from_db()
        self.assertFalse(user.email_verified)
