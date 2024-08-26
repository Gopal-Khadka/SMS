from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Students, AttendanceReport, Courses, Subjects, Attendance


def student_home(request):
    # student_obj = Students.objects.get()
    print(request.user.email)
    return render(request, "student_template/student_home_template.html")
