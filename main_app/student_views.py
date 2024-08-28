from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from pprint import pprint


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


@login_required(login_url="main_app:logInUser")
def show_attendance(request):
    subject_id = 1  # C Pr3ogramming

    # Get the current user
    current_user = CustomUser.objects.get(id=request.user.id)

    # Get the current user's student object
    current_student = Student.objects.get(admin=current_user)

    # Get the attendance report for current student and the given subject
    student_attendance_reports = AttendanceReport.objects.filter(
        student=current_student, attendance__subject__id=subject_id
    )

    # Print or iterate over the attendance records
    attendance_list = []
    for attendance_report in student_attendance_reports:
        _item = {
            "date": attendance_report.attendance.date,
            "status": "Present" if attendance_report.status else "Absent",
            "subject": attendance_report.attendance.subject.name,
        }
        attendance_list.append(_item)
    return render(
        request,
        "student_template/attendance.html",
        {"attendance_list": attendance_list},
    )
