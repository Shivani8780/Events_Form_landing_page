import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Find and optionally delete .mpo files from media directory'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete found .mpo files',
        )

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        mpo_files = []
        for root, dirs, files in os.walk(media_root):
            for file in files:
                if file.lower().endswith('.mpo'):
                    full_path = os.path.join(root, file)
                    mpo_files.append(full_path)

        if not mpo_files:
            self.stdout.write(self.style.SUCCESS('No .mpo files found in media directory.'))
            return

        self.stdout.write(f'Found {len(mpo_files)} .mpo files:')
        for f in mpo_files:
            self.stdout.write(f' - {f}')

        if options['delete']:
            for f in mpo_files:
                try:
                    os.remove(f)
                    self.stdout.write(self.style.SUCCESS(f'Deleted {f}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to delete {f}: {e}'))
        else:
            self.stdout.write('Run with --delete to remove these files.')
