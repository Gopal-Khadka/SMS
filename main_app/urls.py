from django.urls import path
from . import views

app_name = "main_app"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.logInUser, name="logInUser"),
    path("logout", views.logOutUser, name="logOutUser"),
    path("contact", views.contact, name="contact"),
    path("services", views.services, name="services"),
]
