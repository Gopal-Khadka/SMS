from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField, PasswordInput
from .models import CustomUser
from django import forms


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")
        field_classes = {
            "email": EmailField,
            "password1": PasswordInput,
            "password2": PasswordInput,
        }


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ("email",)
    list_display = ["email"]
    form = CustomUserForm
    add_form = CustomUserForm
    list_display = (
        "email",
        "first_name",
        "date_joined",
        "last_login",
        "is_staff",
    )
    search_fields = ("email",)
    readonly_fields = ("date_joined", "last_login")

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        return self.form


admin.site.register(CustomUser, CustomUserAdmin)
