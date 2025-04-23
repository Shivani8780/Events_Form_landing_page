from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import CandidateBiodataForm
from .models import CandidateBiodata
import openpyxl
import os
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from twilio.rest import Client

import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

def save_to_excel(instance):
    file_path = os.path.join(settings.BASE_DIR, 'biodata_records.xlsx')
    if os.path.exists(file_path):
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        headers = [field.name for field in instance._meta.fields if field.name != 'id']
        ws.append(headers)

    data = []
    for field in instance._meta.fields:
        if field.name != 'id':
            value = getattr(instance, field.name)
            if field.name == 'photograph':
                value = value.url if value else ''
            data.append(str(value))
    ws.append(data)
    wb.save(file_path)
    return file_path

def send_confirmation_email(instance, excel_path):
    subject = 'Biodata Form Submission Confirmation'
    body = f'Thank you {instance.candidate_name} for submitting your biodata form.'
    email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [instance.email if hasattr(instance, "email") else ''])
    email.attach_file(excel_path)
    email.send()

def generate_pdf(instance):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Biodata Form Submission")
    y -= 40
    p.setFont("Helvetica", 12)
    for field in instance._meta.fields:
        if field.name != 'id':
            label = field.verbose_name.title() if hasattr(field, 'verbose_name') else field.name.replace('_', ' ').title()
            value = getattr(instance, field.name)
            if field.name == 'photograph':
                value = value.url if value else 'No Photo'
            p.drawString(50, y, f"{label}: {value}")
            y -= 20
            if y < 50:
                p.showPage()
                y = height - 50
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def upload_pdf_to_public_url(pdf_buffer):
    # Generate a unique filename
    filename = f"biodata_pdf_{uuid.uuid4().hex}.pdf"
    # Save the PDF buffer to the default storage (e.g., MEDIA_ROOT)
    path = default_storage.save(filename, ContentFile(pdf_buffer.read()))
    # Construct the full URL to access the file
    if settings.DEBUG:
        # In debug mode, assume media files are served at /media/
        url = settings.MEDIA_URL + filename
    else:
        # In production, you should configure your media URL accordingly
        url = settings.MEDIA_URL + filename
    return url

def send_whatsapp_message(to_number, pdf_buffer):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    media_url = upload_pdf_to_public_url(pdf_buffer)  # Now implemented
    message = client.messages.create(
        body="Thank you for submitting your biodata form. Please find the attached PDF.",
        from_='whatsapp:' + settings.TWILIO_WHATSAPP_NUMBER,
        to='whatsapp:' + to_number,
        media_url=[media_url]
    )
    return message.sid

def biodata_form(request):
    if request.method == 'POST':
        form = CandidateBiodataForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            excel_path = save_to_excel(instance)
            send_confirmation_email(instance, excel_path)
            pdf_buffer = generate_pdf(instance)
            whatsapp_sid = None
            try:
                whatsapp_sid = send_whatsapp_message(instance.whatsapp_number, pdf_buffer)
            except Exception as e:
                whatsapp_sid = f"Failed to send WhatsApp message: {str(e)}"
            return render(request, 'biodata/confirmation.html', {
                'candidate': instance,
                'email_sent': True,
                'whatsapp_sid': whatsapp_sid,
            })
    else:
        form = CandidateBiodataForm()
    return render(request, 'biodata/form.html', {'form': form})

# Note: You need to implement upload_pdf_to_public_url to upload the PDF to a publicly accessible URL
# or use a service that supports media upload for WhatsApp messages.
