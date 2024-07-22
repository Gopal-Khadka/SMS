from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='main_app:logInUser')
def index(request):
    return render(request, "main_app/index.html")

@login_required(login_url='main_app:logInUser')
def contact(request):
    return render(request, "main_app/contact.html")

@login_required(login_url='main_app:logInUser')
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
