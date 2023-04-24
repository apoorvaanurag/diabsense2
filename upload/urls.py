from django.urls import path
from . import views
# from '../results' import views as rv
# from results import views
# add import for barchart
from results.views import barchart


urlpatterns = [
    path("", views.image_request, name="image_request"),
    # add path to barchart view in project/results/urls.py
    path("results", barchart, name="results"),
]
