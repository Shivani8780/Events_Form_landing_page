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

@admin.action(description='Export selected biodata records to Excel with embedded photographs')
def export_to_excel(modeladmin, request, queryset):
    import os
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
                import logging
                logging.error(f"Failed to embed image for row {row_num}: {e}")
        row_num += 1

    wb.save(response)
    return response

class GalleryImageAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(config_name='custom'))

    class Meta:
        model = GalleryImage
        fields = '__all__'

@admin.register(CandidateBiodata)
class CandidateBiodataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CandidateBiodata._meta.fields if field.name != 'id']
    actions = [export_to_excel]

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    form = GalleryImageAdminForm
    list_display = ['title', 'uploaded_at', 'description_display']

    def description_display(self, obj):
        # Render description with inline style for font size
        return format_html('<div style="font-size:14px;">{}</div>', obj.description)
    description_display.short_description = 'Description'
