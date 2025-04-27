from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import CandidateBiodataForm
from .models import CandidateBiodata
import openpyxl
import os
from io import BytesIO
from django.http import HttpResponse, HttpResponseBadRequest
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

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
    # Removed attachment of biodata record as per user request
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

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid

def upload_pdf_to_public_url(pdf_buffer):
    # Generate a unique filename
    filename = f"biodata_pdf_{uuid.uuid4().hex}.pdf"
    # Save the PDF buffer to the default storage (e.g., MEDIA_ROOT)
    path = default_storage.save(f"photographs/{filename}", ContentFile(pdf_buffer.read()))
    # Construct the full public URL using the PUBLIC_BASE_URL from settings
    url = f"{settings.PUBLIC_BASE_URL}/media/photographs/{filename}"
    return url

def send_whatsapp_message(to_number, media_url):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="Thank you for submitting your biodata form. Please find the attached PDF.",
        from_= settings.TWILIO_WHATSAPP_NUMBER,
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
                # Log the public URL of the PDF for debugging
                public_pdf_url = upload_pdf_to_public_url(pdf_buffer)
                # Ensure the URL uses https and the correct PUBLIC_BASE_URL
                if public_pdf_url.startswith('http://localhost'):
                    public_pdf_url = public_pdf_url.replace('http://localhost:8000', settings.PUBLIC_BASE_URL)
                print(f"Public PDF URL: {public_pdf_url}")
                # Pass the public URL to the send_whatsapp_message function
                whatsapp_sid = send_whatsapp_message(instance.whatsapp_number, public_pdf_url)
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

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        incoming_msg = request.POST.get('Body', '').strip().lower()
        from_number = request.POST.get('From', '')
        response = MessagingResponse()
        msg = response.message()

        if 'hello' in incoming_msg:
            msg.body("Hi! Thanks for messaging. How can I help you today?")
        elif 'help' in incoming_msg:
            msg.body("You can submit your biodata form at our website.")
        else:
            msg.body("Sorry, I didn't understand that. Please type 'help' for assistance.")

        return HttpResponse(str(response), content_type='application/xml')
    else:
        return HttpResponseBadRequest("Invalid request method.")

# Note: You need to implement upload_pdf_to_public_url to upload the PDF to a publicly accessible URL
# or use a service that supports media upload for WhatsApp messages.
