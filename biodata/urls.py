from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    # Removed separate form page path as form is handled in home_page
    # path('form/', views.biodata_form, name='biodata_form'),
    path('download-pdf/<int:candidate_id>/', views.download_biodata_pdf, name='download_biodata_pdf'),
    path('confirmation/<int:candidate_id>/', views.confirmation_page, name='confirmation'),
    path('confirmation/', views.confirmation_redirect, name='confirmation_redirect'),
    path('gallery/', views.gallery_page, name='gallery_page'),
    path('contact-us/', views.contact_us_page, name='contact_us_page'),
    path('about-us/', views.about_us_page, name='about_us_page'),
    path('advance-pass-booking/', views.advance_pass_booking, name='advance_pass_booking'),
    path('advance-booklet-booking/', views.advance_booklet_booking, name='advance_booklet_booking'),
    path('advance-booklet-booking/confirmation/<int:booking_id>/', views.advance_booklet_booking_confirmation, name='advance_booklet_booking_confirmation'),
    path('stage-registration/', views.stage_registration, name='stage_registration'),
    path('stage-registration/confirmation/<int:registration_id>/', views.stage_registration_confirmation, name='stage_registration_confirmation'),
    path('spot-advance-booklet/', views.spot_advance_booklet_view, name='spot_advance_booklet'),
    path('spot-advance-booklet/confirmation/<int:booking_id>/', views.spot_advance_booklet_confirmation, name='spot_advance_booklet_confirmation'),
]
