from django import forms
from .models import StudentDetails, LoginDetails


class RegistrationForm(forms.ModelForm):          # student details form (unchanged)
    class Meta:
        model = StudentDetails
        fields = "__all__"


class RegisterForm(forms.ModelForm):              # creates an account
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = LoginDetails
        fields = ["email", "password"]
        widgets = {"password": forms.PasswordInput()}

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("confirm_password"):
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned


class LoginForm(forms.Form):                      # plain Form, not ModelForm
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())