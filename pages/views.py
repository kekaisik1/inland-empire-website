"""Contact form submission handler."""

from __future__ import annotations

import logging
import os

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django_ratelimit.decorators import ratelimit

from .forms import ContactForm

logger = logging.getLogger(__name__)

UTM_KEYS = [
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
    "gclid",
    "gad_source",
    "gad_campaignid",
]


@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def contact_submit(request: HttpRequest) -> HttpResponse:
    """Process contact form submission with UTM attribution."""
    # Derive locale-aware contact page URL from the current request path
    contact_url = request.path.rsplit("submit/", 1)[0] or "/contact/"
    if request.method != "POST":
        return redirect(contact_url)

    form = ContactForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        phone = form.cleaned_data.get("phone", "")
        message_text = form.cleaned_data["message"]

        # Capture UTM attribution from hidden form fields
        utm_data = {
            key: request.POST.get(key, "") for key in UTM_KEYS if request.POST.get(key)
        }

        subject = f"Contact form: {name}"
        body = (
            f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message_text}"
        )

        if utm_data:
            body += "\n\n--- Attribution ---"
            for key, value in utm_data.items():
                body += f"\n{key}: {value}"

        try:
            # Send notification to business
            business_email = os.environ.get(
                "CONTACT_EMAIL", getattr(settings, "DEFAULT_FROM_EMAIL", "")
            )

            if business_email:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=None,  # uses DEFAULT_FROM_EMAIL
                    recipient_list=[business_email],
                    fail_silently=False,
                )
            else:
                logger.warning(
                    "No CONTACT_EMAIL configured — contact form submission lost"
                )

            messages.success(request, _("Thank you! We'll get back to you shortly."))
        except Exception:
            logger.exception("Failed to send contact form email")
            messages.success(
                request,
                _(
                    "Thank you! We received your message and will get back to you shortly."
                ),
            )
    else:
        messages.error(request, _("Please correct the errors below and try again."))

    return redirect(contact_url)
