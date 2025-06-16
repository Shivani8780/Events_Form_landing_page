from django.core.management.base import BaseCommand
import os
from django.conf import settings
import cloudinary
import cloudinary.uploader
from biodata.models import CandidateBiodata

class Command(BaseCommand):
    help = "Migrate local CandidateBiodata images to Cloudinary and update their model URLs."

    def handle(self, *args, **options):
        # Configure Cloudinary using Django settings
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
            api_secret=settings.CLOUDINARY_STORAGE['API_SECRET']
        )

        migrated = 0
        skipped = 0
        not_found = 0

        for obj in CandidateBiodata.objects.all():
            photo_field = obj.photograph
            if photo_field and not str(photo_field).startswith("http"):
                local_path = os.path.join(settings.MEDIA_ROOT, str(photo_field))
                if os.path.exists(local_path):
                    self.stdout.write(f"Migrating: {local_path}")
                    try:
                        result = cloudinary.uploader.upload(local_path)
                        obj.photograph = result['secure_url']
                        obj.save()
                        self.stdout.write(self.style.SUCCESS(f"Done: {obj.photograph}"))
                        migrated += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Failed to upload {local_path}: {e}"))
                        skipped += 1
                else:
                    self.stdout.write(self.style.WARNING(f"File not found: {local_path}"))
                    not_found += 1

        self.stdout.write(self.style.SUCCESS(f"\nMigration finished!"))
        self.stdout.write(self.style.SUCCESS(f"Migrated: {migrated}"))
        self.stdout.write(self.style.WARNING(f"Skipped (errors): {skipped}"))
        self.stdout.write(self.style.WARNING(f"Not found: {not_found}"))
