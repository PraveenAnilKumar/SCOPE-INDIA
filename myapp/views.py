from functools import wraps

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import RegistrationForm, RegisterForm, LoginForm
from .models import LoginDetails


def session_login_required(view_func):
    """Redirect to the login page if the user hasn't logged in."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if "account_id" not in request.session:
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper


@session_login_required
def home(request):
    account = LoginDetails.objects.get(id=request.session["account_id"])
    return render(request, "home.html", {"account": account})

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


def register(request):                     # create account
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        account = form.save(commit=False)
        account.set_password(form.cleaned_data["password"])
        account.save()
        messages.success(request, "Account created. Please log in.")
        return redirect("login")
    return render(request, "register.html", {"form": form})


def login_view(request):
    if "account_id" in request.session:
        return redirect("home")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        account = LoginDetails.objects.filter(email=email).first()
        if account and account.check_password(password):
            request.session["account_id"] = account.id
            return redirect("home")

        messages.error(request, "Invalid email or password.")
    return render(request, "login.html", {"form": form})


def logout_view(request):
    request.session.flush()
    return redirect("login")