from django import forms
from .models import Student, Course, Subject, CustomUser


class SubjectSelectionForm(forms.Form):
    subjects = forms.ModelChoiceField(queryset=None)

    def __init__(self, student: Student, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subjects_queryset = Subject.objects.filter(course=student.course.id)
        self.fields["subjects"].queryset = subjects_queryset


class StudentProfileEditForm(forms.ModelForm):
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
        self.instance = student
        self.fields["email"].initial = (
            student.admin.email
        )  # set saved email as default value in input
        self.fields["dob"].initial = student.dob
        self.fields["parents_num"].initial = student.parents_num
        self.fields["gender"].initial = student.admin.gender

    def save(self, commit=True):
        """
        Saves the student's profile changes to the database.

        Args:
            commit (bool): If True, saves the changes to the database. Defaults to True.

        Returns:
            Student: The updated student instance.

        """
        student = self.instance
        student.admin.email = self.cleaned_data["email"]  # get submitted email
        student.dob = self.cleaned_data["dob"]  # get submitted dob
        student.parents_num = self.cleaned_data[
            "parents_num"
        ]  # get submitted parents_num
        student.admin.gender = self.cleaned_data["gender"]  # get submitted gender
        if commit:
            student.admin.save()  # save email and gender in customuser model
            student.save()  # save dob and parents_num in student model
        return student

    class Meta:
        model = Student
        fields = ()
