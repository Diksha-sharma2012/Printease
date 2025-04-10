import datetime
import os
from pathlib import Path
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm

from django.contrib.auth.decorators import login_required, user_passes_test

from .models import FilesUpload, Order, UserModel
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail



######################################SIGNIN-LOGIN#########################################


# Signup View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import SignUpForm, CustomLoginForm  # Assuming these are custom forms


# Signup View
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if UserModel.objects.filter(email=email).exists():
                messages.error(request, "Email is already in use. Please use a different one.")
            else:
                try:
                    user = form.save(commit=False)
                    user.save()
                    messages.success(request, "Account created successfully! You can now log in.")
                    return redirect('login')
                except IntegrityError:
                    messages.error(request, "Something went wrong while creating your account. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()

    return render(request, 'HUGLI-1-2-3/signin-login/signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            request.session.save()  # Ensure session is saved

            response = HttpResponseRedirect(reverse('services'))
            response.set_cookie('email', user.email, max_age=3600)
            print("User after login:", request.user)
            return response
        else:
            messages.error(request, "Invalid email or password. Please try again.")
    else:
        form = CustomLoginForm()
    return render(request, 'HUGLI-1-2-3/signin-login/login.html', {'form': form})



def logout_view(request):
    print("Before Logout (Incoming Request Cookies):", request.COOKIES)
    if request.method == 'GET':
        print("get")
    else:
        print("Post")
    # Logout user and clear session
    logout(request)
    request.session.flush()
    response = HttpResponseRedirect(reverse('index'))
    print("After Logout (Response Cookies):", response.cookies)
    return response


# Forget password
def forgot_password_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = UserModel.objects.filter(email=email)
            if users.exists():
                for user in users:
                    subject = "Reset Your Password"
                    email_template = "password_reset_email.html"
                    context = {
                        "email": user.email,
                        "domain": request.get_host(),
                        "site_name": "PrintEase",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": 'https' if request.is_secure() else 'http',
                    }
                    message = render_to_string(email_template, context)
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                messages.success(request, "A password reset link has been sent to your email.")
                return redirect('password_reset_done')
            else:
                messages.error(request, "No user found with this email.")
    else:
        form = PasswordResetForm()
    return render(request, "forgot_password.html", {"form": form})





##########################FRONTEND###########################################


def index_view(request):
    print("User:", request.user)  # Check user object
    print("Is Authenticated:", request.user.is_authenticated)
    return render(request, 'HUGLI-1-2-3/frontend/INDEX.html')


def services_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/services.html')


def about_us_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/about-us.html')

def contact_us_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/contact.html')


def atm_pouches_view(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("/printease/login/")

        image_file = request.FILES.get("design_file")  # "design_file" must match the form field name

        if not image_file:
            return render(request, 'HUGLI-1-2-3/frontend/atm-pouches.html', {
                "error": "No file uploaded"
            })

        user = request.user

        # Ensure user has an ID (user is saved in DB)
        if not user.id:
            return render(request, 'HUGLI-1-2-3/frontend/atm-pouches.html', {
                "error": "User does not exist in the database"
            })

        # Create user-specific upload path
        image_path = f"{settings.MEDIA_ROOT}/{user.id}"
        Path(image_path).mkdir(parents=True, exist_ok=True)

        # Save the file manually
        file_path = f"{image_path}/{image_file.name}"
        with open(file_path, "wb") as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # Save file path in DB
        relative_path = f"{user.id}/{image_file.name}"

        user_model = UserModel.objects.get(id=user.id)
        # Create and save database entry
        document = FilesUpload.objects.create(file=relative_path, user=user_model)
        document.save()

        return render(request, 'HUGLI-1-2-3/frontend/upload_success.html')

    return render(request, 'HUGLI-1-2-3/frontend/atm-pouches.html')
def digital_paper_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/digital-paper.html')

def envelopes_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/envelopes.html')

def files_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/files.html')

def garment_tags_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/garment-tags.html')

def order_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/order.html')

def pamphlets_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/pamphlets.html')

def visiting_cards_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/visiting-cards.html')


def pens_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/pens.html')

def stickers_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/stickers-labels.html')

def letter_heads_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/letter-heads.html')

def shooting_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/targets.html')

def bill_books_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/bill-books.html')

@login_required
def checkout_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        notes = request.POST.get('notes')
        product_name = request.POST.get('product', 'Selected Item 1')
        quantity = request.POST.get('quantity', 1)

        user = request.user
        user_model = UserModel.objects.get(id=user.id)
        print(name)
        print(email)
        print(phone)
        print(address)
        print(pincode)
        print(notes)
        print(product_name)
        print(quantity)
        # Save order
        order = Order(
            name=name,
            email=email,
            phone=phone,
            address=address,
            pincode=pincode,
            notes=notes,
            product_name=product_name,
            quantity=quantity,
            user = user_model
        )
        order.save()
        return render(request, 'HUGLI-1-2-3/frontend/services.html')  # Redirect to a confirmation page
    return render(request, 'HUGLI-1-2-3/frontend/checkout.html')

@login_required
def order_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/order.html')





############################## DASHBOARD ##################################

def admin_dashboard(request):
    return render(request, 'HUGLI-1-2-3/dashboard/admin_dashboard.html')

# Helper: check if user is staff (admin)
def is_admin(user):
    return user.is_staff

# Admin dashboard users view
# @login_required
# @user_passes_test(is_admin)
def view_users(request):
    users = UserModel.objects.all().order_by('-date_joined')
    return render(request, 'HUGLI-1-2-3/dashboard/view_users.html', {'users': users})

def delete_user(request, user_id):
    user = get_object_or_404(UserModel, id=user_id)
    if user and not user.is_superuser:
     user.delete()
    return redirect('view-users')


def view_orders(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'HUGLI-1-2-3/dashboard/view_orders.html', {'orders': orders})

def view_uploaded_files(request):
    files = FilesUpload.objects.select_related('user').all()
    # for file in files:
    #  print(file.useemail)
    return render(request, 'HUGLI-1-2-3/dashboard/uploaded_files.html', {'files': files})

def files_with_users_view(request):
    files = FilesUpload.objects.all()
    return render(request, 'files_table.html', {'files': files})

def delete_uploaded_file(request, file_id):
    file = get_object_or_404(FilesUpload, id=file_id)
    file.file.delete()
    file.delete()
    return redirect('view-uploaded-files')


def delete_uploaded_file(request, file_id):
    file = get_object_or_404(FilesUpload, id=file_id)
    file.delete()
    return redirect('view-uploaded-files')


