from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import CandidateBiodataForm
from .models import CandidateBiodata
from biodata.views_weasyprint import generate_pdf

def home_page(request):
    return render(request, 'biodata/home.html')

def biodata_form(request):
    personal_fields = [field.name for field in CandidateBiodata._meta.fields if field.name != 'id']
    if request.method == 'POST':
        form = CandidateBiodataForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            pdf_buffer = generate_pdf(instance)
            # You can save or email the PDF as needed here
            return redirect('confirmation', candidate_id=instance.id)
    else:
        form = CandidateBiodataForm()
    # Add debug print to check rendering
    print("Rendering biodata form page")
    debug_message = "DEBUG: Rendering form_updated.html template"
    return render(request, 'biodata/form_updated.html', {'form': form, 'personal_fields': personal_fields, 'debug_message': debug_message})

def download_biodata_pdf(request, candidate_id):
    instance = get_object_or_404(CandidateBiodata, id=candidate_id)
    pdf_buffer = generate_pdf(instance)
    pdf_buffer.seek(0)
    return FileResponse(pdf_buffer, as_attachment=True, filename='biodata.pdf')

from django.core.mail import EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def confirmation_page(request, candidate_id):
    candidate = get_object_or_404(CandidateBiodata, id=candidate_id)
    whatsapp_group_link = "https://chat.whatsapp.com/BltytlRjrZm1HWYvhley24"
    email_sent = True
    try:
        pdf_buffer = generate_pdf(candidate)
        pdf_buffer.seek(0)
        email = EmailMessage(
            subject='Your Biodata Submission Confirmation',
            body='Thank you for submitting your biodata. Please find the attached PDF.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[candidate.email],
        )
        email.attach('biodata.pdf', pdf_buffer.read(), 'application/pdf')
        email.send(fail_silently=False)
    except Exception as e:
        logger.error(f"Failed to send confirmation email to {candidate.email}: {e}")
        email_sent = False
    return render(request, 'biodata/confirmation.html', {'candidate': candidate, 'whatsapp_group_link': whatsapp_group_link, 'email_sent': email_sent})

def confirmation_redirect(request):
    return HttpResponseRedirect(reverse('home_page'))

from .models import CandidateBiodata, GalleryImage

def gallery_page(request):
    # Query all gallery images from the database
    images = GalleryImage.objects.all()
    return render(request, 'biodata/gallery.html', {'images': images})

def contact_us_page(request):
    # Render the contact us page
    return render(request, 'biodata/contact_us.html')
