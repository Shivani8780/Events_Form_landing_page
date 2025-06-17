from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import CandidateBiodataForm
from .models import CandidateBiodata
from biodata.views_weasyprint import generate_pdf

from .forms import CandidateBiodataForm

def home_page(request):
    if request.method == 'POST':
        form = CandidateBiodataForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            pdf_buffer = generate_pdf(instance)
            # You can save or email the PDF as needed here
            # Redirect after POST to avoid resubmission on refresh
            return redirect('confirmation', candidate_id=instance.id)
        else:
            # Form invalid, render home page with form and errors
            # Add a flag to indicate form errors for template use
            return render(request, 'biodata/home.html', {'form': form, 'form_errors': True})
    else:
        form = CandidateBiodataForm()
    return render(request, 'biodata/home.html', {'form': form})

def biodata_form(request):
    # Deprecated: form handled in home_page now
    return redirect('home_page')

def download_biodata_pdf(request, candidate_id):
    instance = get_object_or_404(CandidateBiodata, id=candidate_id)
    try:
        pdf_buffer = generate_pdf(instance)
        pdf_buffer.seek(0)
        return FileResponse(pdf_buffer, as_attachment=True, filename='biodata.pdf')
    except FileNotFoundError:
        # Handle missing image file gracefully
        return HttpResponse("Error: Some image files are missing. Please contact support.", status=404)

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
            body='\n\nThank you for submitting your biodata form. We have received your details successfully.\n\nRegards,\nBhudev Network Vivah Team'.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[candidate.email],
        )
        # email.attach('biodata.pdf', pdf_buffer.read(), 'application/pdf')
        email.send(fail_silently=False)
    except Exception as e:
        logger.error(f"Failed to send confirmation email to {candidate.email}: {e}")
        email_sent = False
        # Add detailed error message to context for debugging
        return render(request, 'biodata/confirmation.html', {
            'candidate': candidate,
            'whatsapp_group_link': whatsapp_group_link,
            'email_sent': email_sent,
            'error_message': str(e),
        })
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

def about_us_page(request):
    # Render the about us page
    return render(request, 'biodata/about_us.html')
