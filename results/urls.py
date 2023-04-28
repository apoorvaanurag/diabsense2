from django.urls import path
from . import views
# get upload views
from upload.views import image_request




urlpatterns = [
    path("", views.barchart),
    # add path to go to upload
    path("", image_request),
]