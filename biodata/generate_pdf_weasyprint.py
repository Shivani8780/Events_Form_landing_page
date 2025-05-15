import os
from io import BytesIO
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings

def generate_pdf(instance):
    # Render the dedicated PDF template with instance context
    html_string = render_to_string('biodata/pdf_biodata.html', {'instance': instance})

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
