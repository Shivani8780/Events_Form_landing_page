import os
import logging
from django.contrib import admin
from django.http import HttpResponse
import openpyxl
from openpyxl.drawing.image import Image as OpenpyxlImage
from django import forms
from django.utils.html import format_html
import io
import zipfile
import re
import sys
import mimetypes
from .models import CandidateBiodata, GalleryImage
from ckeditor.widgets import CKEditorWidget

# Add missing mimetype for .mpo files to avoid KeyError in openpyxl
def add_custom_mimetypes():
    # Regular handling for Python < 3.13
    mimetypes.add_type('image/mpo', '.mpo')
    
    # Special handling for Python 3.13+
    if sys.version_info >= (3, 13):
        if not hasattr(mimetypes, '_custom_types_map'):
            mimetypes._custom_types_map = {}
        mimetypes._custom_types_map['.mpo'] = 'image/mpo'
        try:
            if hasattr(mimetypes, 'types_map'):
                new_types_map = dict(mimetypes.types_map)
                new_types_map['.mpo'] = 'image/mpo'
                mimetypes.types_map = new_types_map
                if hasattr(mimetypes, '_types_map'):
                    mimetypes._types_map = new_types_map
        except Exception as e:
            logging.error(f"Error setting MIME type for .mpo: {e}")

add_custom_mimetypes()

@admin.action(description='Export selected biodata records to Excel with embedded photographs')
def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=biodata_records_with_photos.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.active

    headers = [field.name for field in CandidateBiodata._meta.fields if field.name != 'id']
    headers.append('image_found')
    ws.append(headers)

    photo_col_idx = headers.index('photograph') + 1
    ws.column_dimensions[openpyxl.utils.get_column_letter(photo_col_idx)].width = 20
    image_found_col_idx = headers.index('image_found') + 1
    ws.column_dimensions[openpyxl.utils.get_column_letter(image_found_col_idx)].width = 15

    row_num = 2
    for obj in queryset:
        row = []
        image_found = 'No'
        for field in CandidateBiodata._meta.fields:
            if field.name != 'id':
                if field.name == 'photograph':
                    row.append('')
                else:
                    value = getattr(obj, field.name)
                    row.append(str(value))

        photo_field = getattr(obj, 'photograph')
        img_path = None
        if photo_field:
            try:
                img_path = photo_field.path
                if os.path.exists(img_path):
                    image_found = 'Yes'
                else:
                    logging.warning(f"Image file not found for row {row_num}: {img_path}")
            except Exception as e:
                logging.error(f"Error checking image file for row {row_num}: {e}")
        
        row.append(image_found)
        ws.append(row)

        if photo_field and image_found == 'Yes' and img_path:
            try:
                img = OpenpyxlImage(img_path)
                img.width = 80
                img.height = 80
                img.anchor = f"{openpyxl.utils.get_column_letter(photo_col_idx)}{row_num}"
                ws.add_image(img)
                ws.row_dimensions[row_num].height = 60
            except Exception as e:
                logging.error(f"Failed to embed image for row {row_num}: {e}")
        
        row_num += 1

    try:
        wb.save(response)
    except Exception as e:
        logging.error(f"Error saving Excel file: {e}")

    return response

@admin.action(description='Download selected candidate images as zip')
def download_selected_images(modeladmin, request, queryset):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for idx, obj in enumerate(queryset, start=1):
            photo_field = getattr(obj, 'photograph')
            if photo_field and photo_field.name:
                try:
                    img_path = photo_field.path
                    if os.path.exists(img_path):
                        candidate_name = re.sub(r'[^a-zA-Z0-9_-]', '_', obj.candidate_name.strip())
                        mobile_number = re.sub(r'[^0-9]', '', obj.registrant_mobile or '')
                        dob_value = obj.dob
                        dob_str = dob_value.strftime('%d%m%Y') if hasattr(dob_value, 'strftime') else 'unknownDOB'
                        serial_number = idx
                        ext = os.path.splitext(img_path)[1]
                        filename = f"{serial_number}_{candidate_name}_{dob_str}_{mobile_number}{ext}"
                        with open(img_path, 'rb') as img_file:
                            img_data = img_file.read()
                        logging.info(f"Adding file to zip: {filename}")
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
    def get_list_display(self, request):
        fields = [field.name for field in CandidateBiodata._meta.fields if field.name not in ('id', 'visa_status_details')]
        if 'visa_status' not in fields:
            return fields
        visa_index = fields.index('visa_status')
        list_display = fields[:visa_index] + ['visa_status'] + fields[visa_index+1:]
        new_list_display = []
        for field_name in list_display:
            if field_name == 'kuldevi':
                new_list_display.append('any_disability_details')
            else:
                new_list_display.append(field_name)
        return new_list_display

    actions = [export_to_excel, download_selected_images]

    def any_disability_details(self, obj):
        return obj.kuldevi
    any_disability_details.short_description = 'Any Disability/Details'

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    form = GalleryImageAdminForm
    list_display = ['title', 'uploaded_at', 'description_display']

    def description_display(self, obj):
        return format_html('<div style="font-size:14px;">{}</div>', obj.description)
    description_display.short_description = 'Description'