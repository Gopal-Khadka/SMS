from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
# Register your models here.
from .models import CustomUser, AdminHOD, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, LeaveReportStaff, FeedBackStudent, FeedBackStaffs, NotificationStudent, NotificationStaffs 

# Register your models here. 
class UserModel(UserAdmin): 
	pass


admin.site.register(CustomUser, UserModel)  # connects the CustomUser model to a custom set of admin features defined in the UserModel class

admin.site.register(AdminHOD) 
admin.site.register(Staffs) 
admin.site.register(Courses) 
admin.site.register(Subjects) 
admin.site.register(Students) 
admin.site.register(Attendance) 
admin.site.register(AttendanceReport) 
admin.site.register(LeaveReportStudent) 
admin.site.register(LeaveReportStaff) 
admin.site.register(FeedBackStudent) 
admin.site.register(FeedBackStaffs) 
admin.site.register(NotificationStudent) 
admin.site.register(NotificationStaffs) 