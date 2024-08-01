from django.urls import path
from . import views
# from . import student_views

app_name = "main_app"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.logInUser, name="logInUser"),
    path("logout", views.logOutUser, name="logOutUser"),
    path("contact", views.contact, name="contact"),
    path("services", views.services, name="services"),
    path("dashboard", views.dashboard, name="dashboard"),
    
    # URLS for Student 
	# path('student_home/', student_views.student_home, name="student_home"), 
	# path('student_view_attendance/', student_views.student_view_attendance, name="student_view_attendance"), 
	# path('student_view_attendance_post/', student_views.student_view_attendance_post, name="student_view_attendance_post"), 
	# path('student_apply_leave/', student_views.student_apply_leave, name="student_apply_leave"), 
	# path('student_apply_leave_save/', student_views.student_apply_leave_save, name="student_apply_leave_save"), 
	# path('student_feedback/', student_views.student_feedback, name="student_feedback"), 
	# path('student_feedback_save/', student_views.student_feedback_save, name="student_feedback_save"), 
	# path('student_profile/', student_views.student_profile, name="student_profile"), 
	# path('student_profile_update/', student_views.student_profile_update, name="student_profile_update"), 
	# path('student_view_result/', student_views.student_view_result, name="student_view_result"), 
]
