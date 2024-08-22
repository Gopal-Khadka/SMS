from django.contrib import admin
from .models import *


# Register your models here.
class UserModel(admin.ModelAdmin):
    ordering = ("email",)
    list_display = [
        "email",
        "user_type",
        "gender",
        "profile_pic",
        "address",
        "created_at",
        "updated_at",
    ]


admin.site.register(
    CustomUser, UserModel
)  # connects the CustomUser model to a custom set of admin features defined in the UserModel class

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
