from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import StudentProfileEditForm
from .student_views import return_current_student


@login_required(login_url="main_app:logInUser")
def index(request):
    return render(request, "main_app/index.html")


@login_required(login_url="main_app:logInUser")
def menu(request):
    return render(request, "main_app/menu.html")


@login_required(login_url="main_app:logInUser")
def contact(request):
    return render(request, "main_app/contact.html")


@login_required(login_url="main_app:logInUser")
def services(request):
    return render(request, "main_app/services.html")


def logInUser(request):
    context = {"today": datetime.today().year}
    if request.user.is_authenticated:
        return redirect("main_app:index")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user=user)
            return redirect("main_app:index")
        else:
            return redirect("main_app:logInUser")
    return render(request, "main_app/login.html", context)


def logOutUser(request):
    logout(request)
    return redirect("main_app:logInUser")


@login_required(login_url="main_app:logInUser")
def menu(request):
    user_types = {"1": "Admin", "2": "Staff", "3": "Student"}
    user_type = user_types[str(request.user.user_type)]
    match (request.user.user_type):
        case "3":
            current_student = return_current_student(request)
            form = StudentProfileEditForm(student=current_student)
            return render(
                request,
                "student_template/home.html",
                context={"user": request.user, "user_type": user_type, "form": form},
            )
        case _:
            return render(request, "main_app/menu.html")
