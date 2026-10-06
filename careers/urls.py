from django.urls import path

from . import views


app_name = "careers"

urlpatterns = [
    # صفحة التقديم على الوظائف.
    path("", views.apply, name="apply"),
]