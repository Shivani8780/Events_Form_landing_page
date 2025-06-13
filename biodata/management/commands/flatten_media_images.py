import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Flatten media images by moving all images from subdirectories to the main media folder'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        self.stdout.write(f"Starting to flatten images in media directory: {media_root}")

        for root, dirs, files in os.walk(media_root, topdown=False):
            if root == media_root:
                # Skip the root directory itself
                continue
            for filename in files:
                src_path = os.path.join(root, filename)
                dest_path = os.path.join(media_root, filename)
                if os.path.exists(dest_path):
                    # Find a new filename with suffix
                    name, ext = os.path.splitext(filename)
                    counter = 1
                    while True:
                        new_filename = f"{name}_{counter}{ext}"
                        new_dest_path = os.path.join(media_root, new_filename)
                        if not os.path.exists(new_dest_path):
                            dest_path = new_dest_path
                            break
                        counter += 1
                shutil.move(src_path, dest_path)
                self.stdout.write(f"Moved {src_path} to {dest_path}")
            # After moving files, remove empty directories
            if not os.listdir(root):
                os.rmdir(root)
                self.stdout.write(f"Removed empty directory {root}")

        self.stdout.write("Flattening media images completed.")
