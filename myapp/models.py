from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
import random
from django.conf import settings
from django.utils import timezone

class LoginDetails(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)   # stores the hash
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email



class EmailOTP(models.Model):
    login = models.OneToOneField(LoginDetails, on_delete=models.CASCADE)
    code = models.CharField(max_length=128)       # stores the hash of the OTP
    created_at = models.DateTimeField(default=timezone.now)
    attempts = models.PositiveSmallIntegerField(default=0)

    def set_code(self, raw_code):
        self.code = make_password(raw_code)

    def check_code(self, raw_code):
        return check_password(raw_code, self.code)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

    def seconds_until_resend(self):
        wait = self.created_at + timedelta(seconds=settings.OTP_RESEND_SECONDS) - timezone.now()
        return max(0, int(wait.total_seconds()))

    @staticmethod
    def generate_code():
        return f"{random.SystemRandom().randint(0, 999999):06d}"



class StudentDetails(models.Model):
    
    class Gender(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'
        OTHER = 'Other', 'Other'

    class Courses(models.TextChoices):
        PHP_FULL_STACK = "PHP Full Stack", "PHP Full Stack"
        PYTHON_FULL_STACK = "Python Full Stack", "Python Full Stack"
        JAVA_FULL_STACK = "Java Full Stack", "Java Full Stack"
        CSHARP_FULL_STACK = "C#.NET Core 7 Full Stack", "C#.NET Core 7 Full Stack"
        MEAN_FULL_STACK = "MEAN Full Stack", "MEAN Full Stack"
        MERN_FULL_STACK = "MERN Full Stack", "MERN Full Stack"
        DATA_SCIENCE_AI = "Data Science & AI", "Data Science & AI"
        DATA_SCIENCE_GENAI = "Data Science - Gen AI", "Data Science - Gen AI"
        PYTHON_MASTERY = "Python Mastery", "Python Mastery"
        FLUTTER = "Flutter Mobile App Development", "Flutter Mobile App Development"
        UI_UX = "UI/UX Designing", "UI/UX Designing"
        DIGITAL_MARKETING = "Digital Marketing Master Program", "Digital Marketing Master Program"
    
    class TrainingMode(models.TextChoices):
        LIVE_ONLINE = "Live online", "Live online"
        CLASSROOM = "Classroom", "Classroom"
    
    class Location(models.TextChoices):
        TECHNOPARk_TVM = "Technopark TVM", "Technopark TVM"
        THAMPANOOR_TVM = "hampanoor TVM", "Thampanoor TVM"
        KOCHI = "Kochi", "Kochi"
        NAGERCOIL = "Nagercoil", "Nagercoil"
        ONLINE = "Online", "Online"
    
    class TrainingTime(models.TextChoices):
        BETWEEN_8AM_10AM = "Between 8am - 10am", "Between 8am - 10am"
        BETWEEN_9AM_1PM = "Between 9am - 1pm", "Between 9am - 1pm"
        BETWEEN_1PM_6PM = "Between 1am - 6pm", "Between 1pm - 6pm"
        BETWEEN_6PM_10PM = "Between 6pm - 10pm", "Between 6pm - 10pm"

    name = models.CharField(max_length=50, null=False)

    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, null=False)
    
    gender = models.CharField(max_length=10, choices=Gender.choices, null=False)
    
    qualification = models.CharField(max_length=50)

    mobile_number = models.CharField(max_length=10, null=False)

    email = models.EmailField(null=False)

    guardian_name = models.CharField(max_length=50)

    guardian_occupation = models.CharField(max_length=20)

    guardian_mobile = models.CharField(max_length=10)

    courses = models.CharField(max_length=100, choices=Courses.choices, null=False)

    training_mode = models.CharField(max_length=50, choices=TrainingMode.choices, null=False)

    location = models.CharField(max_length=50, choices=Location.choices, null=False)

    timing = models.CharField(max_length=50, choices=TrainingTime.choices, null=False)

    address = models.CharField(max_length=200)

    country = models.CharField(max_length=50)

    state = models.CharField(max_length=50)

    city = models.CharField(max_length=50)

    pin = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "StudentDetails"

    def __str__(self):
        return self.name
