from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)  # primary key
    session_start_year = models.DateField()  # start date of the session year
    session_end_year = models.DateField()  # end date of the session year
    objects = (
        models.Manager()
    )  # model manager for the objects (not actually required by default)


# Overriding the Default Django Auth
# User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    # adds the extra field "user_type"
    USER_TYPE = [("1", "HOD"), ("2", "Staff"), ("3", "Student")]
    GENDER = [("M", "Male"), ("F", "Female")]

    username = None
    email = models.EmailField(unique=True)
    user_type = models.CharField(default="1", choices=USER_TYPE, max_length=2)
    gender = models.CharField(max_length=1, choices=GENDER, default="M")
    profile_pic = models.ImageField(upload_to="media/profile_pic", null=True)
    address = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = verbose_name + "s"


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="adminhod"
    )  # if the linked CustomUser instance is deleted, the AdminHOD instance will also be deleted.
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # updates when instance is created
    updated_at = models.DateTimeField(
        auto_now=True
    )  # updates when the instance is updated
    objects = models.Manager()  # provides model functions like all(), get(), filter()

    class Meta:
        verbose_name = "AdminHOD"
        verbose_name_plural = verbose_name + "s"

    def __str__(self):
        return self.admin.email


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="staff"
    )  # map 1 on 1 to custom user
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = verbose_name + "s"

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name


class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = verbose_name + "s"


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)

    # need to give default course (default = 1)
    course_id = models.ForeignKey(
        Courses, on_delete=models.CASCADE, default=1
    )  # use foreign key to establish many to one relationship with "Courses" model
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_name

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = verbose_name + "s"


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="student"
    )
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(
        SessionYearModel, null=True, on_delete=models.CASCADE
    )  # map many to one with "SessionYearModel"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = verbose_name + "s"

    def __str__(self):
        return self.admin.get_full_name()


class Attendance(models.Model):
    # Subject Attendance
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(
        Subjects, on_delete=models.DO_NOTHING
    )  # no action will be taken when a referenced Subjects instance is deleted
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# When the student applies for the leave
class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# When the staff applies for the leave
class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# When the student provides the feedback
class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# When the staff provides the feedback
class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Feedback Staff"
        verbose_name_plural = verbose_name + "s"


# Notifications/notices only for the student
class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Notifications/notices only for the student
class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Notification Staff"
        verbose_name_plural = verbose_name + "s"


# Result
class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE, default=1)
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a user profile when a CustomUser is created.
    If user_type is 1, create an AdminHOD profile.
    If user_type is 2, create a Staffs profile.
    If user_type is 3, create a Students profile.
    """
    if created:
        if instance.user_type == "1":
            AdminHOD.objects.create(admin=instance)
        elif instance.user_type == "2":
            Staffs.objects.create(admin=instance)
        elif instance.user_type == "3":
            Students.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the related object (AdminHOD, Staffs, or Students) when a CustomUser is saved.
    If user_type is 1, save the related AdminHOD object.
    If user_type is 2, save the related Staffs object.
    If user_type is 3, save the related Students object.
    """

    if instance.user_type == "1":  # HOD
        instance.adminhod.save()
    elif instance.user_type == "2":  # Staff
        instance.staff.save()
    elif instance.user_type == "3":  # Student
        instance.student.save()
