from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('form/', views.biodata_form, name='biodata_form'),
    path('download-pdf/<int:candidate_id>/', views.download_biodata_pdf, name='download_biodata_pdf'),
    path('confirmation/<int:candidate_id>/', views.confirmation_page, name='confirmation'),
    path('confirmation/', views.confirmation_redirect, name='confirmation_redirect'),
    path('gallery/', views.gallery_page, name='gallery_page'),
    path('contact-us/', views.contact_us_page, name='contact_us_page'),
]
