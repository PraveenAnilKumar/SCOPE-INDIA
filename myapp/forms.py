from django import forms
from .models import StudentDetails, LoginDetails


class RegistrationForm(forms.ModelForm):          # student details form (unchanged)
    class Meta:
        model = StudentDetails
        fields = "__all__"


class RegisterForm(forms.Form):                   # account creation (plain Form)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if LoginDetails.objects.filter(email__iexact=email, is_verified=True).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("confirm_password"):
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned


class OTPForm(forms.Form):                        # email verification code
    code = forms.CharField(
        label="Verification code",
        min_length=6,
        max_length=6,
        widget=forms.TextInput(attrs={
            "class": "otp-input",
            "inputmode": "numeric",
            "autocomplete": "one-time-code",
            "placeholder": "000000",
        }),
    )


class LoginForm(forms.Form):                      # plain Form, not ModelForm
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())