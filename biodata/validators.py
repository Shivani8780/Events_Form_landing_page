import os
from django.core.exceptions import ValidationError

def validate_not_mpo(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext == '.mpo':
        raise ValidationError("Uploading .mpo files is not supported. Please upload a different image format.")
