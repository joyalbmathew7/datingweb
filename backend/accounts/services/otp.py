import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from accounts.models import EmailOTP,PasswordResetToken


OTP_EXPIRY_MINUTES = 5
MAX_OTP_ATTEMPTS = 5
RESEND_COOLDOWN_SECONDS = 60


class OTPService:

    @staticmethod
    def _hash_otp(otp):
        return hashlib.sha256(
            otp.encode()
        ).hexdigest()

    @staticmethod
    def generate_otp():
        return f"{secrets.randbelow(1_000_000):06d}"

    @staticmethod
    def send_email_otp(user, purpose):
        now = timezone.now()

        recent_otp = (
            EmailOTP.objects
            .filter(
                user=user,
                purpose=purpose,
                created_at__gte=now - timedelta(
                    seconds=RESEND_COOLDOWN_SECONDS
                ),
            )
            .order_by("-created_at")
            .first()
        )

        if recent_otp:
            raise ValidationError(
                "Please wait before requesting another OTP."
            )

        # Invalidate previous OTPs of this purpose
        EmailOTP.objects.filter(
            user=user,
            purpose=purpose,
            is_used=False,
        ).update(is_used=True)

        otp = OTPService.generate_otp()

        EmailOTP.objects.create(
            user=user,
            otp_hash=OTPService._hash_otp(otp),
            purpose=purpose,
            expires_at=now + timedelta(
                minutes=OTP_EXPIRY_MINUTES
            ),
        )

        if purpose == EmailOTP.Purpose.EMAIL_VERIFICATION:
            subject = "Your Kindred verification code"
            message = (
                f"Your Kindred verification code is: {otp}\n\n"
                f"This code expires in {OTP_EXPIRY_MINUTES} minutes."
            )

        elif purpose == EmailOTP.Purpose.PASSWORD_RESET:
            subject = "Your Kindred password reset code"
            message = (
                f"Your Kindred password reset code is: {otp}\n\n"
                f"This code expires in {OTP_EXPIRY_MINUTES} minutes."
            )

        else:
            raise ValidationError("Invalid OTP purpose.")

        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(
                settings,
                "DEFAULT_FROM_EMAIL",
                "noreply@kindred.com",
            ),
            recipient_list=[user.email],
            fail_silently=False,
        )

    @staticmethod
    def verify_email_otp(user, otp, purpose):
        otp = otp.strip()

        if not otp.isdigit() or len(otp) != 6:
            raise ValidationError(
                "OTP must be a 6-digit number."
            )

        otp_record = (
            EmailOTP.objects
            .filter(
                user=user,
                purpose=purpose,
                is_used=False,
            )
            .order_by("-created_at")
            .first()
        )

        if not otp_record:
            raise ValidationError(
                "No active OTP found."
            )

        if otp_record.expires_at < timezone.now():
            otp_record.is_used = True
            otp_record.save(update_fields=["is_used"])

            raise ValidationError(
                "OTP has expired."
            )

        if otp_record.attempts >= MAX_OTP_ATTEMPTS:
            otp_record.is_used = True
            otp_record.save(update_fields=["is_used"])

            raise ValidationError(
                "Too many incorrect attempts."
            )

        otp_record.attempts += 1
        otp_record.save(update_fields=["attempts"])

        if not secrets.compare_digest(
            otp_record.otp_hash,
            OTPService._hash_otp(otp),
        ):
            raise ValidationError(
                "Invalid OTP."
            )

        otp_record.is_used = True
        otp_record.save(update_fields=["is_used"])

        return True

    @staticmethod
    def create_password_reset_token(user):
        token = secrets.token_urlsafe(32)

        token_hash = hashlib.sha256(
            token.encode()
        ).hexdigest()

        PasswordResetToken.objects.update_or_create(
            user=user,
            defaults={
                "token_hash": token_hash,
                "expires_at": timezone.now() + timedelta(
                    minutes=10
                ),
            },
        )

        return token

    @staticmethod
    def verify_password_reset_token(user, token):
        reset_token = (
            PasswordResetToken.objects
            .filter(user=user)
            .first()
        )

        if not reset_token:
            raise ValidationError(
                "Invalid or expired password reset token."
            )

        if reset_token.expires_at < timezone.now():
            reset_token.delete()

            raise ValidationError(
                "Invalid or expired password reset token."
            )

        token_hash = hashlib.sha256(
            token.encode()
        ).hexdigest()

        if not secrets.compare_digest(
            reset_token.token_hash,
            token_hash,
        ):
            raise ValidationError(
                "Invalid or expired password reset token."
            )

        return reset_token

    @staticmethod
    def create_password_reset_token(user):
        token = secrets.token_urlsafe(32)

        token_hash = hashlib.sha256(
            token.encode()
        ).hexdigest()

        PasswordResetToken.objects.update_or_create(
            user=user,
            defaults={
                "token_hash": token_hash,
                "expires_at": timezone.now() + timedelta(
                    minutes=10
                ),
            },
        )

        return token

    @staticmethod
    def verify_password_reset_token(user, token):
        reset_token = (
            PasswordResetToken.objects
            .filter(user=user)
            .first()
        )

        if not reset_token:
            raise ValidationError(
                "Invalid or expired password reset token."
            )

        if reset_token.expires_at < timezone.now():
            reset_token.delete()

            raise ValidationError(
                "Invalid or expired password reset token."
            )

        token_hash = hashlib.sha256(
            token.encode()
        ).hexdigest()

        if not secrets.compare_digest(
            reset_token.token_hash,
            token_hash,
        ):
            raise ValidationError(
                "Invalid or expired password reset token."
            )

        return reset_token