"""Contact form with validation."""

from __future__ import annotations

import re

from django import forms
from django.core.validators import RegexValidator

_PHONE_RE = re.compile(r"^[\d\s\-\(\)\+\.]{7,20}$")
phone_validator = RegexValidator(
    regex=_PHONE_RE,
    message="Enter a valid phone number (digits, spaces, dashes, parentheses).",
)


class ContactForm(forms.Form):
    """Contact form for the website."""

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your name",
                "class": "w-full px-4 py-3 border border-border rounded-card focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-colors",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "your@email.com",
                "class": "w-full px-4 py-3 border border-border rounded-card focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-colors",
            }
        ),
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone (optional)",
                "type": "tel",
                "class": "w-full px-4 py-3 border border-border rounded-card focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-colors",
            }
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "How can we help?",
                "rows": 4,
                "class": "w-full px-4 py-3 border border-border rounded-card focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-colors resize-y",
            }
        ),
    )
