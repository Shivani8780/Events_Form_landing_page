import os
import requests
from django.core.management.base import BaseCommand
from biodata.models import CandidateBiodata
from django.conf import settings
from urllib.parse import urlparse

class Command(BaseCommand):
    help = 'Migrate Cloudinary images to local storage and update database fields'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        migrated = 0
        skipped = 0

        for obj in CandidateBiodata.objects.all():
            photo_url = str(obj.photograph)
            if photo_url.startswith('http'):
                parsed_url = urlparse(photo_url)
                filename = os.path.basename(parsed_url.path)
                local_path = os.path.join('photographs', filename)
                full_local_path = os.path.join(media_root, local_path)
                os.makedirs(os.path.dirname(full_local_path), exist_ok=True)

                # Download from Cloudinary if not already present
                if not os.path.exists(full_local_path):
                    self.stdout.write(f'Downloading {photo_url} ...')
                    try:
                        response = requests.get(photo_url, timeout=20)
                        response.raise_for_status()
                        with open(full_local_path, 'wb') as f:
                            f.write(response.content)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Failed to download {photo_url}: {e}'))
                        skipped += 1
                        continue

                # Update the database record to point to the new local file
                obj.photograph = local_path
                obj.save(update_fields=['photograph'])
                self.stdout.write(self.style.SUCCESS(f'Updated {obj.pk}: {local_path}'))
                migrated += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f'Complete! {migrated} images migrated, {skipped} already local or skipped.'))
