from . import student_views
from django.urls import path, include

urlpatterns = [
    path("", student_views.home, name="menu"),
]
