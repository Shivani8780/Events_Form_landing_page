from django.urls import path
from . import views

app_name = 'biodata'

urlpatterns = [
    path('', views.biodata_form, name='biodata_form'),
]
