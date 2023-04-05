from django.urls import path
from . import views


urlpatterns = [
    path("", views.image_request, name="image_request"),
]
