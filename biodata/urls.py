from django.urls import path
from . import views

urlpatterns = [
    path('', views.biodata_form, name='biodata_form'),
    path('api/whatsapp/incoming/', views.whatsapp_webhook, name='whatsapp_webhook'),
]
