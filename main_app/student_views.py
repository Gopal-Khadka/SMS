from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url="main_app:logInUser")
def home(request):
    context = {
        "name": request.user.full_name,
        "gender": "Male" if request.user.gender == "M" else "Female",
        "email": request.user.email,
        "user_type": request.user.user_type,
        "profile_pic": request.user.profile_pic.url,
    }
    return render(request, "student_template/home.html", context=context)
