from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/' ,views.logout_view, name='logout'),
    path('index/', views.index_view, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('services/', views.services_view, name='services'),
    path('contactus/', views.contact_us_view, name='contactus'),
    path('atm-pouches/', views.atm_pouches_view, name='atm-pouches'),
    path('digital-paper/', views.digital_paper_view, name='digital-paper'),
    path('envelopes/', views.envelopes_view, name='envelopes'),
    path('files/', views.files_view, name='files'),
    path('garment-tags/', views.garment_tags_view, name='garment-tags'),
    path('order/', views.order_view, name='order'),
    path('pamphlets/', views.pamphlets_view, name='pamphlets'),
    path('visiting-cards/', views.visiting_cards_view, name='visiting-cards'),
    path('aboutus/', views.about_us_view, name='aboutus'),
]

