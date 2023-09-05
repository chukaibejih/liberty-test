from config.settings import DEFAULT_FROM_EMAIL
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
import smtplib

from .models import UserProfile

User = get_user_model()


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens. Sends an email to the user when a token is created.
    """
    context = {
        "current_user": reset_password_token.user,
        "first_name": reset_password_token.user.first_name,
        "email": reset_password_token.user.email,
        "reset_password_url": f"{instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm'))}?token={reset_password_token.key}",
    }

    email_html_message = render_to_string("account/reset_password.html", context)

    subject = "Password Reset for Liberty Blog"
    from_email = DEFAULT_FROM_EMAIL
    to_email = reset_password_token.user.email

    msg = EmailMultiAlternatives(subject, email_html_message, from_email, [to_email])
    msg.send()


@receiver(post_save, sender=User, dispatch_uid="unique_identifier")
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        print("Created")
        try:
            subject = "Confirm Your Email Address"
            verification_url = reverse(
                "confirm-email",
                kwargs={
                    "uidb64": urlsafe_base64_encode(smart_bytes(instance.pk)),
                    "token": default_token_generator.make_token(instance),
                },
            )
            confirmation_link = f"{settings.SITE_DOMAIN}{verification_url}"
            message = render_to_string(
                "account/email_confirmation.html",
                {"user": instance, "confirmation_link": confirmation_link},
            )
            from_email = DEFAULT_FROM_EMAIL
            to_email = instance.email
            send_mail(subject, message, from_email, [to_email], fail_silently=False)

        except smtplib.SMTPException as e:
            return f"Error sending confirmation email: {e}"


# TODO: Make registration atomic.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
