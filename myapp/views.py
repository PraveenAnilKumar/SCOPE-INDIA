from django.shortcuts import render, redirect
from . forms import RegistrationForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contacts(request):
    return render(request, 'contacts.html')

def courses(request):
    return render(request, 'courses.html')

def faq(request):
    return render(request, 'faq.html')

def placements(request):
    return render(request, 'placements.html')
    
def reviews(request):
    return render(request, 'reviews.html')

def faq(request):
    return render(request, 'faq.html')

def reviews(request):
    return render(request, 'reviews.html')

def registration(request):
    form = RegistrationForm()

    if request.method == "POST":
        form = RegistrationForm(request.POST)  
        if form.is_valid():
            form.save()                         
            return redirect('home')             

    return render(request, 'registration.html', {'form': form})