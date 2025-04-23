from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

admin_required = [login_required, staff_member_required]

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index_view, name='index'),
    path('signup/', views.signup_view, name='signup'),

    #Forget password
    # path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #     template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
    #     template_name='password_reset_complete.html'), name='password_reset_complete'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
    #     template_name='password_reset_done.html'), name='password_reset_done'),


###########################FRONTEND####################################################

    path('services/', views.services_view, name='services'),
    path('aboutus/', views.about_us_view, name='aboutus'),
    path('contactus/', views.contact_us_view, name='contactus'),
    path('atm-pouches/', views.atm_pouches_view, name='atm-pouches'),
    path('digital-paper/', views.digital_paper_view, name='digital-paper'),
    path('envelopes/', views.envelopes_view, name='envelopes'),
    path('files/', views.files_view, name='files'),
    path('garment-tags/', views.garment_tags_view, name='garment-tags'),
    path('pamphlets/', views.pamphlets_view, name='pamphlets'),
    path('visiting-cards/', views.visiting_cards_view, name='visiting-cards'),
    path('pens/', views.pens_view, name='pens'),
    path('stickers-labels/', views.stickers_view, name='stickers-labels'),
    path('letter-heads/', views.letter_heads_view, name='letter-heads'),
    path('shooting-targets/', views.shooting_view, name='shooting-targets'),
    path('bill-books/', views.bill_books_view, name='bill-books'),
    path('checkout/', views.checkout_view, name='checkout'),
    # path('order/<str:card_type>/', views.order_view, name='order'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),



############################DASHBOARD################################################

path('admin-login/', views.admin_login, name='admin_login'),

    # Admin Dashboard URLs
    path('admin-dashboard/',
         views.admin_dashboard,
         name='admin-dashboard'),

    # User Management
    path('admin-dashboard/view-users/',
         staff_member_required(views.view_users),
         name='view-users'),
    path('admin-dashboard/delete-user/<int:user_id>/',
         staff_member_required(views.delete_user),
         name='delete-user'),

    # Order Management
    path('admin-dashboard/orders/',
         staff_member_required(views.view_orders),
         name='view-orders'),
    path('admin-dashboard/delete-order/<int:order_id>/',
         staff_member_required(views.delete_order),
         name='delete-order'),

    # File Management
    path('admin-dashboard/view-uploaded-files/',
         staff_member_required(views.view_uploaded_files),
         name='view-uploaded-files'),
    path('admin-dashboard/delete-file/<int:file_id>/',
         staff_member_required(views.delete_uploaded_file),
         name='delete-uploaded-file'),

    # Bill Book Management
    path('admin-dashboard/bill-order/',
         staff_member_required(views.view_billbooks),
         name='view-bill-orders'),
    path('admin-dashboard/delete-order-bill/<int:order_id>/',
         staff_member_required(views.delete_order_bill_letter),
         name='delete-order-bill'),

    # Letterhead Management
    path('admin-dashboard/letter-order/',
         staff_member_required(views.view_letterhead),
         name='view-letter-orders'),
    path('admin-dashboard/delete-order-letter/<int:order_id>/',
         staff_member_required(views.delete_order_letter),
         name='delete-order-letter'),

    # Files Table View
    path('admin-dashboard/files-table/',
         staff_member_required(views.files_with_users_view),
         name='files-table'),

    path('user/dashboard/', views.user_dashboard, name='user-dashboard'),

    path('order/view/general/<int:order_id>/', views.view_orders_user, name='view_order'),

    path('order/view/billbook/<int:order_id>/', views.view_bill_order, name='view_bill_order'),
    path('order/view/letterhead/<int:order_id>/', views.view_letter_order, name='view_letter_order'),
    path('files/', views.view_uploaded_files_user, name='view_uploaded_files'),
    # path('order/cancel/<int:order_id>/<str:order_type>/', views.cancel_order, name='cancel_order'),
     path('base/', views.base_view, name='base' )
]

