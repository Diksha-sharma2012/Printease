from pathlib import Path
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .models import FilesUpload, Order, OrderBillModel, OrderLetterModel
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from .forms import SignUpForm, CustomLoginForm
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods




######################################SIGNIN-LOGIN#########################################
# Signup View
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
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


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()

            # At this point, user is already authenticated by AuthenticationForm logic.
            login(request, user)  # Django handles session creation
            request.session.save()

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
# def forgot_password_view(request):
#     if request.method == "POST":
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             users = UserModel.objects.filter(email=email)
#             if users.exists():
#                 for user in users:
#                     subject = "Reset Your Password"
#                     email_template = "password_reset_email.html"
#                     context = {
#                         "email": user.email,
#                         "domain": request.get_host(),
#                         "site_name": "PrintEase",
#                         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                         "user": user,
#                         "token": default_token_generator.make_token(user),
#                         "protocol": 'https' if request.is_secure() else 'http',
#                     }
#                     message = render_to_string(email_template, context)
#                     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
#                 messages.success(request, "A password reset link has been sent to your email.")
#                 return redirect('password_reset_done')
#             else:
#                 messages.error(request, "No user found with this email.")
#     else:
#         form = PasswordResetForm()
#     return render(request, "forgot_password.html", {"form": form})
#


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
        print("in post")
        if not request.user:
            return redirect("/printease/login/")

        image_file = request.FILES.get("design_file")  # "design_file" must match the form field name
        print("working")
        if not image_file:
            return render(request, 'HUGLI-1-2-3/frontend/atm-pouches.html', {
                "error": "No file uploaded"
            })
        print("image is correct")

        user = request.user

        # Ensure user has an ID (user is saved in DB)
        if not user.id:
            return render(request, 'HUGLI-1-2-3/frontend/atm-pouches.html', {
                "error": "User does not exist in the database"
            })
        print("userid")
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
        user_model = User.objects.get(id=user.id)

        # Create and save database entry
        document = FilesUpload.objects.create(file=relative_path, user=user_model)
        document.save()

        return render(request, 'HUGLI-1-2-3/frontend/upload_success.html')
    else:
        print("error")
    return render(request, 'HUGLI-1-2-3/frontend/atm-pouches.html')


def digital_paper_view(request):
    return render(request, 'HUGLI-1-2-3/frontend/digital-paper.html')


def envelopes_view(request):
    if request.method == "POST":
        envelopes = request.POST.get("envelopes")
        quantity = request.POST.get("quantity")
        return render(request, 'HUGLI-1-2-3/frontend/checkout.html', {'cards': envelopes, "quantity": quantity})
    return render(request, 'HUGLI-1-2-3/frontend/envelopes.html')


def files_view(request):
    if request.method == "POST":
        files = request.POST.get("files")
        quantity = request.POST.get("quantity")
        return render(request, 'HUGLI-1-2-3/frontend/checkout.html', {'cards': files, "quantity": quantity})
    return render(request, 'HUGLI-1-2-3/frontend/files.html')


def garment_tags_view(request):
    if request.method == "POST":
        pamphlet_paper = request.POST.get("garment-tags")
        quantity = request.POST.get("quantity")
        print(pamphlet_paper)
        return render(request, 'HUGLI-1-2-3/frontend/checkout.html', {'cards': pamphlet_paper, "quantity": quantity})
    return render(request, 'HUGLI-1-2-3/frontend/garment-tags.html')


def pamphlets_view(request):
    if request.method == "POST":
        pamphlet_paper = request.POST.get("pamphlet-paper")
        quantity = request.POST.get("quantity")
        print(pamphlet_paper)
        return render(request, 'HUGLI-1-2-3/frontend/checkout.html', {'cards': pamphlet_paper, "quantity": quantity})
    return render(request, 'HUGLI-1-2-3/frontend/pamphlets.html')


def visiting_cards_view(request, ):
    if request.method == "POST":
        product_type = request.POST.get("product_type")
        product_name = request.POST.get("product_name")
        quantity = request.POST.get("quantity")
        print(product_name, product_type)
        return render(request, 'HUGLI-1-2-3/frontend/checkout.html', {'product_type': product_type,
                                                                      "quantity": quantity,
                                                                      "product_name": product_name})
    return render(request, 'HUGLI-1-2-3/frontend/visiting-cards.html')


def pens_view(request):
    if request.method == "POST":
        cards = request.POST.get("pens")
        quantity = request.POST.get("quantity")
        print(quantity)
        return render(request, 'HUGLI-1-2-3/frontend/checkout.html', {'cards': cards, "quantity": quantity})
    return render(request, 'HUGLI-1-2-3/frontend/pens.html')


def stickers_view(request):
    if request.method == "POST":
        card = request.POST.get("card")
        quantity = request.POST.get("quantity")
        print(quantity)
        return render(request, 'HUGLI-1-2-3/frontend/checkout.html', {'cards': card, "quantity": quantity})
    return render(request, 'HUGLI-1-2-3/frontend/stickers.html')



def letter_heads_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        try:
            # Get form data with proper field names
            order_data = {
                'order_type': request.POST.get('order_type', 'Letterhead'),
                'company_name': request.POST.get('company_name'),
                'address': request.POST.get('address'),
                'paper_type': request.POST.get('paper_type'),
                'paper_size': request.POST.get('paper_size'),
                'quantity': request.POST.get('quantity'),
                'logo': request.FILES.get('logo'),
                'user': request.user
            }

            # Validate required fields
            required_fields = ['company_name', 'address', 'paper_type', 'paper_size', 'quantity']
            for field in required_fields:
                if not order_data.get(field):
                    raise ValueError(f"Missing required field: {field}")

            # Create and save order
            letter_head = OrderLetterModel(**order_data)
            letter_head.full_clean()  # Validate model fields
            letter_head.save()

            messages.success(request, 'Order placed successfully!')
            return redirect('letter-heads')

        except Exception as e:
            messages.error(request, f'Error processing order: {str(e)}')
            return redirect('letter-heads')

    # GET request handling
    return render(request, 'HUGLI-1-2-3/frontend/letterhead.html')



def shooting_view(request):
    if request.method == "POST":
        card = request.POST.get("target")
        quantity = request.POST.get("quantity")
        return render(request, 'HUGLI-1-2-3/frontend/checkout.html', {'cards': card, "quantity": quantity})
    return render(request, 'HUGLI-1-2-3/frontend/targets.html')


# views.py

def bill_books_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        # Retrieve form data including the uploaded file
        order_type = request.POST.get('order_type')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        bill_book_order_type = request.POST.get('bill_book_order_type')
        paper_size = request.POST.get('paper_size')
        number_of_books = request.POST.get('number_of_books')
        pages_per_book = request.POST.get('pages_per_book', '')
        logo = request.FILES.get('logo')

        user = request.user

        # Create and save the model instance with the logo
        bill_book = OrderBillModel(
            order_type=order_type,
            company_name=company_name,
            address=address,
            paper_type=bill_book_order_type,
            paper_size=paper_size,
            number_of_book=number_of_books,
            page_per_book=pages_per_book,
            user=user,
            logo=logo
        )
        bill_book.save()  # This will save the file to MEDIA_ROOT/billbook_logos/

        return redirect('bill-books')

    # Fetch all orders for display
    billbook_orders = OrderBillModel.objects.all()
    return render(request, 'HUGLI-1-2-3/frontend/billbooks.html', {'billbook_orders': billbook_orders})



@login_required
def checkout_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        notes = request.POST.get('notes')
        product_type = request.POST.get('product_type', '')
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity', 1)

        user = request.user
        user_model = User.objects.get(id=user.id)

        print(name, "name")
        print(email)
        print(phone)
        print(address)
        print(pincode)
        print(notes)
        print(product_name)
        print(product_type)
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
            product_type=product_type,
            quantity=quantity,
            user=user_model
        )
        order.save()
        return render(request, 'HUGLI-1-2-3/frontend/services.html')
    else:
        print("get")
    return render(request, 'HUGLI-1-2-3/frontend/checkout.html')


############################## DASHBOARD ##################################


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin-dashboard')
        else:
            messages.error(request, 'Invalid credentials or not authorized.')
            return redirect('admin_login')

    return render(request, 'HUGLI-1-2-3/dashboard/admin_login.html')



@staff_member_required
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    return render(request, 'HUGLI-1-2-3/dashboard/admin_dashboard.html')

@staff_member_required
# @login_required
def is_admin(user):
    return user.is_staff


# Admin dashboard users view
@staff_member_required
# @login_required
def view_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'HUGLI-1-2-3/dashboard/view_users.html', {'users': users})


@staff_member_required
# @login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user and not user.is_superuser:
        user.delete()
    return redirect('view-users')


@staff_member_required
# @login_required
def view_orders(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'HUGLI-1-2-3/dashboard/view_orders.html', {'orders': orders})


@staff_member_required
# @login_required
def delete_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.delete()
    return redirect('view-orders')


@staff_member_required
# @login_required
def view_uploaded_files(request):
    files = FilesUpload.objects.select_related('user').all()
    # for file in files:
    #  print(file.useemail)
    return render(request, 'HUGLI-1-2-3/dashboard/uploaded_files.html', {'files': files})


@staff_member_required
# @login_required
def files_with_users_view(request):
    files = FilesUpload.objects.all()
    return render(request, 'files_table.html', {'files': files})


@staff_member_required
# @login_required
def delete_uploaded_file(request, file_id):
    file = get_object_or_404(FilesUpload, id=file_id)
    file.file.delete()
    file.delete()
    return redirect('view-uploaded-files')


@staff_member_required
# @login_required
def delete_uploaded_file(request, file_id):
    file = get_object_or_404(FilesUpload, id=file_id)
    file.delete()
    return redirect('view-uploaded-files')


@staff_member_required
# @login_required
def view_billbooks(request):
    billbook_orders = OrderBillModel.objects.all().order_by('-id')
    return render(request,
                'HUGLI-1-2-3/dashboard/view_billbook.html',
                {'billbook_orders': billbook_orders})


@staff_member_required
@require_http_methods(["POST"])
def delete_order_bill_letter(request, order_id):
    if request.method == 'POST':
        try:
            order = OrderBillModel.objects.get(id=order_id)
            order.delete()
            messages.success(request, 'Bill book order deleted successfully')
        except Exception as e:
            messages.error(request, f'Error deleting order: {str(e)}')
    return redirect('view-bill-orders')



@staff_member_required
def view_letterhead(request):
    letterhead_orders = OrderLetterModel.objects.all().order_by('-id')
    return render(request,
                 'HUGLI-1-2-3/dashboard/view_letterhead.html',
                 {'letterhead_orders': letterhead_orders})

@staff_member_required
@require_http_methods(["POST"])
def delete_order_letter(request, order_id):
    if request.method == 'POST':
        try:
            order = OrderLetterModel.objects.get(id=order_id)
            order.delete()
            messages.success(request, 'Letterhead order deleted successfully')
        except Exception as e:
            messages.error(request, f'Error deleting order: {str(e)}')
    return redirect('view-letter-orders')

