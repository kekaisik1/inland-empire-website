"""Pages URL configuration (contact form)."""

from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path("submit/", views.contact_submit, name="contact_submit"),
]
