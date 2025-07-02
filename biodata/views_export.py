import io
import os
import zipfile
from django.http import HttpResponse
from django.conf import settings
import pandas as pd
from .models import AdvanceBookletBooking

def export_booklet_booking_and_images(request):
    # Query all AdvanceBookletBooking entries
    bookings = AdvanceBookletBooking.objects.all()

    # Prepare data for Excel export
    data = []
    for booking in bookings:
        data.append({
            'Name': booking.name,
            'City': booking.city,
            'Whatsapp Number': booking.whatsapp_number,
            'Email': booking.email,
            'Without Courier': booking.without_courier,
            'Girls Booklet Without': booking.girls_booklet_without,
            'Boys Booklet Without': booking.boys_booklet_without,
            'With Courier': booking.with_courier,
            'Girls Booklet With': booking.girls_booklet_with,
            'Boys Booklet With': booking.boys_booklet_with,
            'Courier Address': booking.courier_address,
            'Total Amount': booking.total_amount,
            'Payment Screenshot': os.path.basename(booking.payment_screenshot.name) if booking.payment_screenshot else '',
        })

    df = pd.DataFrame(data)

    # Create an in-memory Excel file
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Bookings')

    excel_buffer.seek(0)

    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Add Excel file to zip
        zip_file.writestr('booklet_bookings.xlsx', excel_buffer.read())

        # Add payment screenshot images to zip
        for booking in bookings:
            if booking.payment_screenshot:
                image_path = os.path.join(settings.MEDIA_ROOT, booking.payment_screenshot.name)
                if os.path.exists(image_path):
                    zip_file.write(image_path, os.path.basename(image_path))

    zip_buffer.seek(0)

    # Prepare response
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=booklet_bookings_and_images.zip'
    return response
