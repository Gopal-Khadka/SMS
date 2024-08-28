from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import SubjectSelectionForm


def return_current_student(request):
    current_user = CustomUser.objects.get(id=request.user.id)

    # Check if the current user is a student
    current_student = Student.objects.get(
        admin=current_user
    )  # Get the Student instance for the current user

    return current_student


@login_required(login_url="main_app:logInUser")
def show_teachers(request):

    current_student = return_current_student(request)
    # Query all the teachers who teach the subjects associated with the courses the current student is enrolled in
    teachers_teaching_current_user = Staff.objects.filter(
        subjects__course=current_student.course
    ).distinct()

    # Print or iterate over the teachers who teach the current user
    teachers = list(enumerate(teachers_teaching_current_user, start=1))
    context = {
        "teachers": teachers,
        "males_count": len(teachers_teaching_current_user.filter(admin__gender="M")),
        "females_count": len(teachers_teaching_current_user.filter(admin__gender="F")),
    }
    return render(request, "student_template/teachers.html", context)


@login_required(login_url="main_app:logInUser")
def show_classmates(request):

    current_student = return_current_student(request)

    # Get the course and session of the current student
    current_course = current_student.course
    current_session = current_student.session

    # Query for other students in the same course and session
    students_in_same_course_and_session = Student.objects.filter(
        course=current_course, session=current_session
    ).exclude(admin=current_student.admin)

    # Print or iterate over the teachers who teach the current user
    classmates = list(enumerate(students_in_same_course_and_session, start=1))
    context = {
        "classmates": classmates,
        "males_count": len(
            students_in_same_course_and_session.filter(admin__gender="M")
        ),
        "females_count": len(
            students_in_same_course_and_session.filter(admin__gender="F")
        ),
    }
    return render(request, "student_template/classmates.html", context)


@login_required(login_url="main_app:logInUser")
def show_attendance(request):
    current_student = return_current_student(request)

    subject_id = None
    if request.method == "POST":
        form = SubjectSelectionForm(current_student, request.POST)
        if form.is_valid():
            subject_id = form.cleaned_data["subjects"].id
    else:
        form = SubjectSelectionForm(student=current_student)

    # Get the attendance report for current student and the given subject
    if subject_id:
        student_attendance_reports = AttendanceReport.objects.filter(
            student=current_student, attendance__subject__id=subject_id
        )
    else:
        student_attendance_reports = AttendanceReport.objects.filter(
            student=current_student
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

    context = {
        "attendance_list": list(enumerate(attendance_list, start=1)),
        "form": form,
        "present_count": sum(
            1 for item in attendance_list if item["status"] == "Present"
        ),
        "absent_count": sum(
            1 for item in attendance_list if item["status"] == "Absent"
        ),
        "unique_subjects_count": len(set(item["subject"] for item in attendance_list)),
    }
    return render(request, "student_template/attendance.html", context)


@login_required(login_url="main_app:logInUser")
def show_notices(request):
    current_student = return_current_student(request)
    notices = NotificationStudent.objects.filter(student=current_student)
    notices = list(enumerate(notices, start=1))
    return render(request, "student_template/notices.html", {"notices": notices})
