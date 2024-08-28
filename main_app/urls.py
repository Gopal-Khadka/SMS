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
    # urls for student views
    path("menu/", views.menu, name="menu"),
    path(
        "student/show_teachers",
        student_views.show_teachers,
        name="student_show_teachers",
    ),
    path(
        "student/show_classmates",
        student_views.show_classmates,
        name="student_show_classmates",
    ),
    path(
        "student/show_attendance",
        student_views.show_attendance,
        name="student_show_attendance",
    ),
    path(
        "student/show_notices",
        student_views.show_notices,
        name="student_show_notices",
    ),
]
