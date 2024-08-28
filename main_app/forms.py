from django import forms
from .models import Student, Course, Subject


class SubjectSelectionForm(forms.Form):
    subjects = forms.ModelChoiceField(queryset=None)

    def __init__(self, student: Student, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subjects_queryset = Subject.objects.filter(course=student.course.id)
        self.fields["subjects"].queryset = subjects_queryset
