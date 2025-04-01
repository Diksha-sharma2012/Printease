import os
from pathlib import Path

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from .models import PrintEaseSignModel
from .forms import SignUpForm, CustomLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from .models import FilesUpload
from django.conf import settings


# Signup View
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                if User.objects.filter(username=user.username).exists():
                    messages.error(request, "Username already taken. Please choose another.")
                else:
                    user.save()
                    messages.success(request, "Account created successfully! You can now log in.")
                    return redirect('login')  # Redirect after signup
            except IntegrityError:
                messages.error(request, "An error occurred. Please try again.")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = SignUpForm()

    return render(request, 'HUGLI-1/signup.html', {'form': form})


# Login View
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Set cookies
            response = HttpResponseRedirect(reverse('services'))
            response.set_cookie('email', user.email, max_age=3600)  # Expires in 1 hour
            response.set_cookie('password', request.POST.get('password'), max_age=3600)

            messages.success(request, "You have successfully logged in!")
            return response
        else:
            messages.error(request, "Invalid email or password. Please try again.")
    else:
        form = CustomLoginForm()

    return render(request, 'HUGLI-1-2-3/login.html', {'form': form})

def logout_view(request):
    print("Before Logout (Incoming Request Cookies):", request.COOKIES)
    # Logout user and clear session
    logout(request)
    request.session.flush()
    # Redirect to login page
    response = HttpResponseRedirect(reverse('login'))
    # Print debug info (optional)
    print("After Logout (Response Cookies):", response.cookies)
    return response


# Static Pages (Using TemplateView instead of ListView)

def index_view(request):
    return render(request, 'HUGLI-1-2-3/INDEX.html')


def services_view(request):
    return render(request, 'HUGLI-1/services.html')


def about_us_view(request):
    return render(request, 'HUGLI-1/about-us.html')

def contact_us_view(request):
    return render(request, 'HUGLI-1/contact.html')

@login_required
def atm_pouches_view(request):
    return render(request, 'HUGLI-1/atm-pouches.html')

@login_required
def digital_paper_view(request):
    return render(request, 'HUGLI-1/digital-paper.html')

@login_required
def envelopes_view(request):
    return render(request, 'HUGLI-1/envelopes.html')

@login_required
def files_view(request):
    return render(request, 'HUGLI-1/files.html')

@login_required
def garment_tags_view(request):
    return render(request, 'HUGLI-1/garment-tags.html')

@login_required
def order_view(request):
    return render(request, 'HUGLI-1/order.html')

@login_required
def pamphlets_view(request):
    if request.method == "POST":
        image_file = request.FILES["image"]
        print(request.user.id)
        image_path = str(settings.MEDIA_ROOT) + "/"+ str(request.user.id)
        Path(image_path).mkdir(exist_ok=True)
        document = FilesUpload.objects.create(file=image_path + "/" +str(image_file))
        document.save()
        with open(image_path + "/" +str(image_file), 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)
        # return HttpResponse("Your file was uploaded.")
        return render(request, 'HUGLI-1/upload_success.html')
    return render(request, 'HUGLI-1/pamphlets.html')

@login_required
def visiting_cards_view(request):
    return render(request, 'HUGLI-1/visiting-cards.html')

