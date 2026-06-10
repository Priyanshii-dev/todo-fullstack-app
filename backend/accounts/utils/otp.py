import random
from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail


def _otp_key(email: str) -> str:
    return f"otp:{email.lower()}"

def _attempts_key(email: str) -> str:
    return f"otp_attempts:{email.lower()}"


def send_otp(user):
    code = f"{random.randint(0, 999999):06d}"

    # Store OTP with TTL — overwrites any previous code
    cache.set(_otp_key(user.email), code, timeout=settings.OTP_EXPIRY_SECONDS)

    # Reset attempt counter
    cache.delete(_attempts_key(user.email))

    send_mail(
        subject="Your verification code",
        message=(
            f"Hi {user.email},\n\n"
            f"Your OTP is: {code}\n\n"
            f"It expires in {settings.OTP_EXPIRY_SECONDS // 60} minutes.\n"
            "If you didn't request this, ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def verify_otp(email: str, code: str) -> tuple[bool, str]:
    """
    Returns (True, "") on success.
    Returns (False, reason) on failure.
    """
    email = email.strip().lower()
    attempts_key = _attempts_key(email)

    # Brute-force guard
    attempts = cache.get(attempts_key, 0)
    if attempts >= settings.OTP_MAX_ATTEMPTS:
        return False, "Too many attempts. Request a new OTP."

    stored_code = cache.get(_otp_key(email))

    if stored_code is None:
        return False, "OTP expired or not found. Request a new one."

    if stored_code != code.strip():
        # Increment attempt counter (keep same TTL as OTP)
        cache.set(attempts_key, attempts + 1, timeout=settings.OTP_EXPIRY_SECONDS)
        return False, "Invalid OTP."

    # Success — delete both keys immediately
    cache.delete(_otp_key(email))
    cache.delete(attempts_key)
    return True, ""