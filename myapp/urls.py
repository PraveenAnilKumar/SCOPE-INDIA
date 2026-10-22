from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('courses/', views.courses, name='courses'),
    path('placements/', views.placements, name='placements'),
    path('registration/', views.registration, name='registration'),
    path('faq/', views.faq, name='faq'),
    path('reviews/', views.reviews, name='reviews'),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
