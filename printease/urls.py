from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index_view, name='index'),
    path('signup/', views.signup_view, name='signup'),

    #Forget password
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),




    path('services/', views.services_view, name='services'),
    path('aboutus/', views.about_us_view, name='aboutus'),
    path('contactus/', views.contact_us_view, name='contactus'),
    path('atm-pouches/', views.atm_pouches_view, name='atm-pouches'),
    path('digital-paper/', views.digital_paper_view, name='digital-paper'),
    path('envelopes/', views.envelopes_view, name='envelopes'),
    path('files/', views.files_view, name='files'),
    path('garment-tags/', views.garment_tags_view, name='garment-tags'),
    path('order/', views.order_view, name='order'),
    path('pamphlets/', views.pamphlets_view, name='pamphlets'),
    path('visiting-cards/', views.visiting_cards_view, name='visiting-cards'),
    path('pens/', views.pens_view, name='pens'),
    path('stickers-labels/', views.stickers_view, name='stickers-labels'),
    path('letter-heads/', views.letter_heads_view, name='letter-heads'),
    path('shooting-targets/', views.shooting_view, name='shooting-targets'),
    path('bill-books/', views.bill_books_view, name='bill-books'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/', views.order_view, name='order'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin-dashboard/view-users/', views.view_users, name='view-users'),
    path('admin-dashboard/delete-user/<int:user_id>/', views.delete_user, name='delete-user'),
    path('admin-dashboard/orders/', views.view_orders, name='view-orders'),
    path('admin-dashboard/view-uploaded-files/', views.view_uploaded_files, name='view-uploaded-files'),
    path('files-table/', views.files_with_users_view, name='files_table'),
    path('admin-dashboard/delete-file/<int:file_id>/', views.delete_uploaded_file, name='delete_uploaded_file'),








]

