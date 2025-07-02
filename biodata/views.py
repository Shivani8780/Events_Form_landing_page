import io
import os
import zipfile
import pandas as pd
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings

from .forms import CandidateBiodataForm
from .models import CandidateBiodata, AdvancePassBooking, AdvanceBookletBooking, GalleryImage
from biodata.views_weasyprint import generate_pdf
from .forms_advance_pass import AdvancePassBookingForm
from .forms_advance_booklet import AdvanceBookletBookingForm

logger = logging.getLogger(__name__)

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

def advance_pass_booking(request):
    if request.method == 'POST':
        form = AdvancePassBookingForm(request.POST, request.FILES)
        if form.is_valid():
            entry_token_selected = form.cleaned_data.get('entry_token_selected')
            entry_token_qty = int(form.cleaned_data.get('entry_token_quantity', 0)) if entry_token_selected else 0
            tea_coffee_selected = form.cleaned_data.get('tea_coffee_selected')
            tea_coffee_qty = int(form.cleaned_data.get('tea_coffee_quantity', 0)) if tea_coffee_selected else 0
            unlimited_buffet_selected = form.cleaned_data.get('unlimited_buffet_selected')
            unlimited_buffet_qty = int(form.cleaned_data.get('unlimited_buffet_quantity', 0)) if unlimited_buffet_selected else 0

            total_amount = (entry_token_qty * 20 +
                            tea_coffee_qty * 30 +
                            unlimited_buffet_qty * 200)

            # Check for duplicate entry
            existing_booking = AdvancePassBooking.objects.filter(
                email=form.cleaned_data['email'],
                entry_token_quantity=entry_token_qty,
                tea_coffee_quantity=tea_coffee_qty,
                unlimited_buffet_quantity=unlimited_buffet_qty,
            ).first()

            if existing_booking:
                error_message = "A booking with the same details already exists. Duplicate submission is not allowed."
                return render(request, 'biodata/advance_pass_booking.html', {'form': form, 'error_message': error_message})

            advance_pass_booking = AdvancePassBooking(
                name=form.cleaned_data['name'],
                city=form.cleaned_data['city'],
                whatsapp_number=form.cleaned_data['whatsapp_number'],
                email=form.cleaned_data['email'],
                entry_token_quantity=entry_token_qty,
                tea_coffee_quantity=tea_coffee_qty,
                unlimited_buffet_quantity=unlimited_buffet_qty,
                payment_screenshot=form.cleaned_data['payment_screenshot'],
                total_amount=total_amount,
            )
            advance_pass_booking.save()

            # Send confirmation email
            email_subject = 'Advance Pass Booking Confirmation'
            email_body = f"Dear {form.cleaned_data['name']},\n\nThank you for your advance pass booking.\n\nDetails:\n"
            if entry_token_qty > 0:
                email_body += f"Entry Token Pass x {entry_token_qty}\n"
            if tea_coffee_qty > 0:
                email_body += f"Tea - Coffee Pass x {tea_coffee_qty}\n"
            if unlimited_buffet_qty > 0:
                email_body += f"Unlimited Buffet Lunch x {unlimited_buffet_qty}\n"
            email_body += f"Total Amount: ₹{total_amount}\n\nThis booking Confirmation is valid only if your Payment is valid and if we have duly received your Payment as per your information given to us.\n\nRegards,\nEvent Team"
            print(f"Sending email from: {settings.DEFAULT_FROM_EMAIL} to: {form.cleaned_data['email']}")
            email = EmailMessage(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [form.cleaned_data['email']],
            )
            email.send(fail_silently=False)

            return render(request, 'biodata/advance_pass_booking_success.html', {'form': form, 'total_amount': total_amount})
        else:
            return render(request, 'biodata/advance_pass_booking.html', {'form': form})
    else:
        form = AdvancePassBookingForm()
    return render(request, 'biodata/advance_pass_booking.html', {'form': form})


def advance_booklet_booking(request):
    logger.info(f"advance_booklet_booking called with method: {request.method}")
    if request.method == 'POST':
        form = AdvanceBookletBookingForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info("Form is valid")
            total_amount = form.cleaned_data.get('total_amount', 0)

            advance_booklet_booking = form.save(commit=False)
            advance_booklet_booking.total_amount = total_amount
            advance_booklet_booking.with_courier = True
            advance_booklet_booking.save()

            # Send confirmation email
            email_subject = 'Advance Booklet Booking Confirmation'
            email_body = f"Dear {form.cleaned_data['name']},\n\nThank you for your advance booklet booking.\n\nDetails:\n"
            if form.cleaned_data.get('girls_booklet_with'):
                email_body += "Girls Biodata Booklet (With Courier)\n"
            if form.cleaned_data.get('boys_booklet_with'):
                email_body += "Boys Biodata Booklet (With Courier)\n"
            email_body += f"Courier Address: {form.cleaned_data.get('courier_address')}\n"
            email_body += f"Total Amount: ₹{total_amount}\n\nThis booking Confirmation is valid only if your Payment is valid and if we have duly received your Payment as per your information given to us.\n\nRegards,\nEvent Team"
            try:
                logger.info(f"Sending email from: {settings.DEFAULT_FROM_EMAIL} to: {form.cleaned_data['email']}")
                email = EmailMessage(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [form.cleaned_data['email']],
                )
                email.send(fail_silently=False)
            except Exception as e:
                logger.error(f"Failed to send confirmation email: {e}")

            logger.info("Redirecting to confirmation page")
            return redirect('advance_booklet_booking_confirmation', booking_id=advance_booklet_booking.id)
        else:
            logger.info("Form is invalid")
            logger.error(f"Form errors: {form.errors}")
            logger.error(f"Non-field errors: {form.non_field_errors()}")
            return render(request, 'biodata/advance_booklet_booking.html', {'form': form})
    else:
        logger.info("GET request, rendering form")
        form = AdvanceBookletBookingForm()
    return render(request, 'biodata/advance_booklet_booking.html', {'form': form})

def export_booklet_booking_and_images(request):
    bookings = AdvanceBookletBooking.objects.all()
    data = []
    for booking in bookings:
        data.append({
            'Name': booking.name,
            'City': booking.city,
            'Whatsapp Number': booking.whatsapp_number,
            'Email': booking.email,
            'Girls Booklet With': booking.girls_booklet_with,
            'Boys Booklet With': booking.boys_booklet_with,
            'Courier Address': booking.courier_address,
            'Total Amount': booking.total_amount,
            'Payment Screenshot': os.path.basename(booking.payment_screenshot.name) if booking.payment_screenshot else '',
        })

    df = pd.DataFrame(data)

    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Bookings')

    excel_buffer.seek(0)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr('booklet_bookings.xlsx', excel_buffer.read())

        for booking in bookings:
            if booking.payment_screenshot:
                image_path = os.path.join(settings.MEDIA_ROOT, booking.payment_screenshot.name)
                if os.path.exists(image_path):
                    zip_file.write(image_path, os.path.basename(image_path))

    zip_buffer.seek(0)

    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=booklet_bookings_and_images.zip'
    return response

def advance_booklet_booking_confirmation(request, booking_id):
    booking = get_object_or_404(AdvanceBookletBooking, id=booking_id)
    return render(request, 'biodata/advance_booklet_booking_success.html', {'booking': booking})

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

def confirmation_page(request, candidate_id):
    candidate = get_object_or_404(CandidateBiodata, id=candidate_id)
    whatsapp_group_link = "https://chat.whatsapp.com/K2kgtdbwtpu5PWXVkE6RVj"
    email_sent = True
    try:
        pdf_buffer = generate_pdf(candidate)
        pdf_buffer.seek(0)
        email = EmailMessage(
            subject='Your Biodata Submission Confirmation',
            body='\n\nThank you for submitting your biodata form. We have received your details successfully.\n\nRegards,\nBhudev Network Vivah Team.',
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
