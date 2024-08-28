from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField, PasswordInput
from .models import (
    CustomUser,
    Attendance,
    AttendanceReport,
    FeedbackStaff,
    FeedbackStudent,
    Admin,
    Course,
    Session,
    Student,
    Staff,
    Subject,
    LeaveReportStaff,
    LeaveReportStudent,
    NotificationStaff,
    NotificationStudent,
)
from django.utils.translation import gettext_lazy as _


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no email field."""

    model = CustomUser
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "gender",
                    "profile_pic",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "user_type"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff", "user_type")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


admin.site.register(Admin)
admin.site.register(Course)
admin.site.register(Session)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(FeedbackStaff)
admin.site.register(FeedbackStudent)
admin.site.register(Subject)
admin.site.register(LeaveReportStaff)
admin.site.register(LeaveReportStudent)
admin.site.register(NotificationStaff)
admin.site.register(NotificationStudent)