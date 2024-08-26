from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(PermissionsMixin, AbstractBaseUser):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female")]
    USER_TYPE_CHOICES = [("1", "Admin"), ("2", "Teacher"), ("3", "Student")]

    username = None
    email = models.EmailField(max_length=255, unique=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True, default="")
    last_name = models.CharField(max_length=255, blank=True, default="")

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now, blank=True)
    last_login = models.DateTimeField(blank=True, null=True)

    gender = models.CharField(
        max_length=1, blank=True, default="M", choices=GENDER_CHOICES
    )
    user_type = models.CharField(
        max_length=1, blank=True, default="3", choices=USER_TYPE_CHOICES
    )
    updated_at = models.DateTimeField(default=timezone.now, blank=True)
    profile_pic = models.ImageField(upload_to="media/profile_pics", null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email
