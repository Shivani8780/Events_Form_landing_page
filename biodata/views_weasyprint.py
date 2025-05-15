from django.template.loader import render_to_string
from io import BytesIO
import os
from pathlib import Path
import base64
import requests
from django.conf import settings
from weasyprint import HTML, CSS

def generate_pdf(instance):
    # Convert photograph to base64 string by fetching from URL
    photo_data = ''
    if instance.photograph and hasattr(instance.photograph, 'url'):
        try:
            response = requests.get(instance.photograph.url)
            if response.status_code == 200:
                photo_data = base64.b64encode(response.content).decode('utf-8')
        except Exception:
            photo_data = ''

    # Convert logo image to base64 string
    logo_data = ''
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        try:
            with open(logo_path, 'rb') as logo_file:
                logo_data = base64.b64encode(logo_file.read()).decode('utf-8')
        except Exception:
            logo_data = ''

    # Read base64 font data from file
    font_base64_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'font_base64.txt')
    font_base64_data = ''
    if os.path.exists(font_base64_path):
        try:
            with open(font_base64_path, 'r', encoding='utf-8') as font_file:
                font_base64_data = font_file.read().strip()
        except Exception:
            font_base64_data = ''

    # Render the biodata PDF HTML template with instance context, photo_data, logo_data, and font_base64_data
    html_string = render_to_string('biodata/pdf_biodata.html', {
        'instance': instance,
        'photo_data': photo_data,
        'logo_data': logo_data,
        'font_base64_data': font_base64_data,
    })

    # Create a BytesIO buffer to receive PDF data
    pdf_buffer = BytesIO()

    # Define path to CSS file for styling PDF (optional, can create a CSS file for PDF styles)
    css_path = os.path.join(settings.BASE_DIR, 'static', 'css', 'pdf_styles.css')
    css = CSS(filename=css_path) if os.path.exists(css_path) else None

    # Generate PDF from HTML string using WeasyPrint
    if css:
        HTML(string=html_string).write_pdf(target=pdf_buffer, stylesheets=[css])
    else:
        HTML(string=html_string).write_pdf(target=pdf_buffer)

    pdf_buffer.seek(0)
    return pdf_buffer
