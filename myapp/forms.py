from django import forms
from . models import StudentDetails


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = StudentDetails
        fields = "__all__"

