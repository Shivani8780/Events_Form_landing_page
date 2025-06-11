from django.contrib import admin
from django.http import HttpResponse
import openpyxl
from openpyxl.drawing.image import Image as OpenpyxlImage
from .models import CandidateBiodata, GalleryImage
import os
from django.conf import settings
import openpyxl.utils
from django import forms
from ckeditor.widgets import CKEditorWidget
from django.utils.html import format_html
import zipfile
import io
import re
import logging

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
            try:
                img_path = photo_field.path
                img = OpenpyxlImage(img_path)
                # Resize image if needed
                img.width = 80
                img.height = 80
                img.anchor = f"{openpyxl.utils.get_column_letter(photo_col_idx)}{row_num}"
                ws.add_image(img)
                # Adjust row height
                ws.row_dimensions[row_num].height = 60
            except Exception as e:
                logging.error(f"Failed to embed image for row {row_num}: {e}")
        row_num += 1

    wb.save(response)
    return response

@admin.action(description='Download selected candidate images as zip')
def download_selected_images(modeladmin, request, queryset):
    # Create in-memory zip file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for obj in queryset:
            photo_field = getattr(obj, 'photograph')
            if photo_field and photo_field.name:
                try:
                    img_path = photo_field.path
                    if os.path.exists(img_path):
                        # Sanitize candidate name and mobile number for filename
                        candidate_name = re.sub(r'[^a-zA-Z0-9_-]', '_', obj.candidate_name.strip())
                        mobile_number = re.sub(r'[^0-9]', '', obj.registrant_mobile or '')
                        dob_str = obj.dob.strftime('%d%m%Y') if obj.dob else 'unknownDOB'
                        serial_number = obj.id or 'unknownID'
                        ext = os.path.splitext(img_path)[1]
                        filename = f"{serial_number}_{candidate_name}_{dob_str}_{mobile_number}{ext}"
                        with open(img_path, 'rb') as img_file:
                            img_data = img_file.read()
                        zip_file.writestr(filename, img_data)
                except Exception as e:
                    logging.error(f"Failed to add image for candidate {obj.candidate_name}: {e}")
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=selected_candidate_images.zip'
    return response

class GalleryImageAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(config_name='custom'))

    class Meta:
        model = GalleryImage
        fields = '__all__'

@admin.register(CandidateBiodata)
class CandidateBiodataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CandidateBiodata._meta.fields if field.name != 'id']
    actions = [export_to_excel, download_selected_images]

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    form = GalleryImageAdminForm
    list_display = ['title', 'uploaded_at', 'description_display']

    def description_display(self, obj):
        # Render description with inline style for font size
        return format_html('<div style="font-size:14px;">{}</div>', obj.description)
    description_display.short_description = 'Description'

