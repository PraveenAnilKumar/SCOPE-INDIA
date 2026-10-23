from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import LoginForm, OTPForm, RegisterForm, RegistrationForm
from .models import EmailOTP, LoginDetails


# ---------- helpers ----------

def session_login_required(view_func):
    """Redirect to the login page if the user hasn't logged in."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        account_id = request.session.get("account_id")
        if not account_id:
            return redirect("login")

        account = LoginDetails.objects.filter(id=account_id, is_verified=True).first()
        if account is None:                      # deleted or unverified account
            request.session.flush()
            return redirect("login")

        request.account = account                # available in the view
        return view_func(request, *args, **kwargs)
    return wrapper


def send_otp_email(login_obj):
    raw_code = EmailOTP.generate_code()
    otp, _ = EmailOTP.objects.get_or_create(login=login_obj)
    otp.set_code(raw_code)
    otp.attempts = 0
    otp.created_at = timezone.now()
    otp.save()

    send_mail(
        subject="Your verification code",
        message=(
            f"Your verification code is {raw_code}.\n"
            f"It expires in {settings.OTP_EXPIRY_MINUTES} minutes.\n\n"
            "If you didn't sign up, you can ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[login_obj.email],
        fail_silently=False,
    )


# ---------- pages (login required) ----------

@session_login_required
def home(request):
    return render(request, "home.html", {"account": request.account})

@session_login_required
def about(request):
    return render(request, "about.html")

@session_login_required
def contacts(request):
    return render(request, "contacts.html")

@session_login_required
def courses(request):
    return render(request, "courses.html")

@session_login_required
def faq(request):
    return render(request, "faq.html")

@session_login_required
def placements(request):
    return render(request, "placements.html")

@session_login_required
def reviews(request):
    return render(request, "reviews.html")


@session_login_required
def registration(request):                 # student details form
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("home")
    return render(request, "registration.html", {"form": form})


# ---------- account creation + OTP verification ----------

def register(request):                     # create account and send OTP
    if request.session.get("account_id"):
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # reuse an unverified record for this email (verified ones are blocked in the form)
            login_obj, created = LoginDetails.objects.get_or_create(
                email=form.cleaned_data["email"]
            )
            login_obj.set_password(form.cleaned_data["password"])
            login_obj.is_verified = False
            login_obj.save()

            try:
                send_otp_email(login_obj)
            except Exception:
                if created:
                    login_obj.delete()
                messages.error(request, "Could not send the verification email. Please try again.")
                return render(request, "register.html", {"form": form})

            request.session["pending_login_id"] = login_obj.id
            return redirect("verify_otp")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def verify_otp(request):
    login_id = request.session.get("pending_login_id")
    if not login_id:
        return redirect("register")

    login_obj = get_object_or_404(LoginDetails, id=login_id, is_verified=False)
    otp = get_object_or_404(EmailOTP, login=login_obj)

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            if otp.is_expired():
                messages.error(request, "Code expired. Please request a new one.")
            elif otp.attempts >= settings.OTP_MAX_ATTEMPTS:
                messages.error(request, "Too many wrong attempts. Please request a new code.")
            elif otp.check_code(form.cleaned_data["code"]):
                login_obj.is_verified = True
                login_obj.save()
                otp.delete()
                request.session.pop("pending_login_id", None)
                request.session["account_id"] = login_obj.id     # log them in
                return redirect("home")
            else:
                otp.attempts += 1
                otp.save()
                messages.error(request, "Invalid code.")
    else:
        form = OTPForm()

    return render(request, "verify_otp.html", {
        "form": form,
        "email": login_obj.email,
        "wait": otp.seconds_until_resend(),
    })


def resend_otp(request):
    login_id = request.session.get("pending_login_id")
    if not login_id:
        return redirect("register")

    login_obj = get_object_or_404(LoginDetails, id=login_id, is_verified=False)
    otp = EmailOTP.objects.filter(login=login_obj).first()

    if otp and otp.seconds_until_resend() > 0:
        messages.error(request, f"Please wait {otp.seconds_until_resend()}s before requesting another code.")
    else:
        try:
            send_otp_email(login_obj)
            messages.success(request, "A new code has been sent.")
        except Exception:
            messages.error(request, "Could not send the email. Please try again.")
    return redirect("verify_otp")


# ---------- login / logout ----------

def login_view(request):
    if request.session.get("account_id"):
        return redirect("home")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].strip().lower()
        password = form.cleaned_data["password"]

        account = LoginDetails.objects.filter(email__iexact=email).first()

        if not account or not account.check_password(password):
            messages.error(request, "Invalid email or password.")
        elif not account.is_verified:
            # correct password but email not verified: send a fresh code
            try:
                send_otp_email(account)
                request.session["pending_login_id"] = account.id
                messages.error(request, "Please verify your email first. We sent a new code.")
                return redirect("verify_otp")
            except Exception:
                messages.error(request, "Could not send the verification email.")
        else:
            request.session["account_id"] = account.id
            return redirect("home")

    return render(request, "login.html", {"form": form})


def logout_view(request):
    request.session.flush()
    return redirect("login")