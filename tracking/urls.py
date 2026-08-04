"""URL routing for privacy-aware tracking APIs."""

from django.urls import path

from . import views

app_name = "tracking"

urlpatterns = [
    path("collect/", views.collect, name="collect"),
    path(
        "webhooks/booking-complete/",
        views.booking_complete,
        name="booking_complete",
    ),
]
