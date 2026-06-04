import logging
import threading

from django.conf import settings
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def _send_email(subject, html_message, recipient_email):
    """Send email in a background thread to avoid blocking the request."""
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info("Welcome email sent to %s", recipient_email)
    except Exception as e:
        logger.error("Failed to send welcome email to %s: %s", recipient_email, e)


@receiver(post_save, sender=User)
def user_registered(sender, instance, created, **kwargs):
    """Signal fired after a new user registers — sends a welcome email."""
    if created:
        logger.info("New user registered: %s", instance.email)

        context = {
            "email": instance.email,
            "login_url": getattr(settings, "FRONTEND_URL", "http://localhost:3000") + "/login",
        }

        html_message = render_to_string("emails/welcome.html", context)

        email_thread = threading.Thread(
            target=_send_email,
            args=("Welcome to TaskFlow!", html_message, instance.email),
        )
        email_thread.start()
