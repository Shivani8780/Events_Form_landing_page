import os
from django.conf import settings
from biodata.models import CandidateBiodata
import cloudinary.uploader

for obj in CandidateBiodata.objects.all():
    if obj.photograph and not str(obj.photograph).startswith("http"):
        local_path = os.path.join(settings.MEDIA_ROOT, str(obj.photograph))
        if os.path.exists(local_path):
            result = cloudinary.uploader.upload(local_path)
            obj.photograph = result['secure_url']
            obj.save()
