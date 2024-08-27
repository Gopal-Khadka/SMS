from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *


@login_required(login_url="main_app:logInUser")
def show_teachers(request):
    current_user = CustomUser.objects.get(id=request.user.id)

    # Check if the current user is a student
    current_student = Student.objects.get(
        admin=current_user
    )  # Get the Student instance for the current user

    # Query all the teachers who teach the subjects associated with the courses the current student is enrolled in
    teachers_teaching_current_user = Staff.objects.filter(
        subject__course=current_student.course
    ).distinct()

    # Print or iterate over the teachers who teach the current user
    teachers = [teacher.admin.full_name for teacher in teachers_teaching_current_user]

    return render(
        request, "student_template/teachers.html", context={"teachers": teachers}
    )


@login_required(login_url="main_app:logInUser")
def show_classmates(request):

    # Get the current user's user_type and session year from the database
    current_user = CustomUser.objects.get(id=request.user.id)

    # Get the current user's student object
    current_student = Student.objects.get(admin=current_user)

    # Get the course and session of the current student
    current_course = current_student.course
    current_session = current_student.session

    # Query for other students in the same course and session
    students_in_same_course_and_session = Student.objects.filter(
        course=current_course, session=current_session
    ).exclude(admin=current_user)

    # Print or iterate over the teachers who teach the current user
    classmates = [
        student.admin.full_name for student in students_in_same_course_and_session
    ]

    return render(
        request, "student_template/classmates.html", context={"classmates": classmates}
    )
