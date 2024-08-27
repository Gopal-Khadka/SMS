from django.urls import path, include
from . import views
from . import student_views

app_name = "main_app"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.logInUser, name="logInUser"),
    path("logout", views.logOutUser, name="logOutUser"),
    path("contact", views.contact, name="contact"),
    path("services", views.services, name="services"),
    path("menu/",include('main_app.menu_urls')), 
    # urls for student views
    # path("student_home/", student_views.home, name="student_home"),
]
