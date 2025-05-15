from django.contrib import admin
from django.http import HttpResponse
import openpyxl
from openpyxl.drawing.image import Image as OpenpyxlImage
from .models import CandidateBiodata, GalleryImage
import os
from django.conf import settings
import openpyxl.utils

@admin.action(description='Export selected biodata records to Excel with embedded photographs')
def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=biodata_records_with_photos.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.active

    # Write headers
    headers = [field.name for field in CandidateBiodata._meta.fields if field.name != 'id']
    ws.append(headers)

    # Set column width for photograph column (assuming last column)
    photo_col_idx = headers.index('photograph') + 1
    ws.column_dimensions[openpyxl.utils.get_column_letter(photo_col_idx)].width = 20

    # Write data rows
    row_num = 2
    for obj in queryset:
        row = []
        for field in CandidateBiodata._meta.fields:
            if field.name != 'id':
                if field.name == 'photograph':
                    # Placeholder for image, will insert after
                    row.append('')
                else:
                    value = getattr(obj, field.name)
                    row.append(str(value))
        ws.append(row)

        # Insert image if exists
        photo_field = getattr(obj, 'photograph')
        if photo_field:
            # photo_field is a CloudinaryResource object, get URL instead of name
            try:
                import logging
                import ssl
                from urllib.request import urlopen
                import tempfile
                import os
                # Download image from Cloudinary URL with SSL context to ignore certificate verification
                img_url = photo_field.url
                logging.info(f"Downloading image from URL: {img_url}")
                try:
                    context = ssl._create_unverified_context()
                    image_data = urlopen(img_url, timeout=10, context=context).read()
                except Exception as ssl_e:
                    logging.error(f"SSL error while downloading image: {ssl_e}")
                    # Fallback without SSL context (not recommended)
                    image_data = urlopen(img_url, timeout=10).read()
                # Save to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                    tmp_file.write(image_data)
                    tmp_file_path = tmp_file.name
                img = OpenpyxlImage(tmp_file_path)
                # Resize image if needed
                img.width = 80
                img.height = 80
                img.anchor = f"{openpyxl.utils.get_column_letter(photo_col_idx)}{row_num}"
                ws.add_image(img)
                # Adjust row height
                ws.row_dimensions[row_num].height = 60
                # Remove the temporary file after adding image
                # Delay deletion to ensure image is loaded by openpyxl
                import threading
                import time
                def delayed_delete(path):
                    time.sleep(5)
                    try:
                        os.unlink(path)
                    except Exception as e:
                        import logging
                        logging.error(f"Failed to delete temp image file {path}: {e}")
                threading.Thread(target=delayed_delete, args=(tmp_file_path,)).start()
            except Exception as e:
                import logging
                logging.error(f"Failed to embed image for row {row_num}: {e}")
        row_num += 1

    wb.save(response)
    return response

@admin.register(CandidateBiodata)
class CandidateBiodataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CandidateBiodata._meta.fields if field.name != 'id']
    actions = [export_to_excel]

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at']
