from django import forms
from .models import Student, Course, Subject, CustomUser


class SubjectSelectionForm(forms.Form):
    subjects = forms.ModelChoiceField(queryset=None)

    def __init__(self, student: Student, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subjects_queryset = Subject.objects.filter(course=student.course.id)
        self.fields["subjects"].queryset = subjects_queryset


class StudentProfileEditForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "value": "new@email.com"}
        ),
    )
    dob = forms.DateField(
        label="Date Of Birth",
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    parents_num = forms.CharField(
        label="Parent's Contact",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    gender = forms.ChoiceField(
        label="Gender",
        required=False,
        choices=CustomUser.GENDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, student: Student, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].initial = student.admin.email
        self.fields["dob"].initial = student.dob
        self.fields["parents_num"].initial = student.parents_num
        self.fields["gender"].initial = student.admin.gender

    class Meta:
        model = Student  # denotes that this form is for model "Student"
