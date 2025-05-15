from django.core.management.base import BaseCommand
from biodata.models import CandidateBiodata
from biodata.views_weasyprint import generate_pdf
import tempfile

class Command(BaseCommand):
    help = 'Test PDF generation for CandidateBiodata'

    def handle(self, *args, **options):
        instance = CandidateBiodata.objects.first()
        if not instance:
            self.stdout.write(self.style.ERROR('No CandidateBiodata instance found. Please create one first.'))
            return

        pdf_file = generate_pdf(instance)
        import os
        temp_dir = tempfile.gettempdir()
        # Use current working directory instead of temp directory to avoid permission issues
        temp_path = os.path.join(os.getcwd(), 'test_biodata.pdf')
        try:
            with open(temp_path, 'wb') as f:
                f.write(pdf_file.read())
            self.stdout.write(self.style.SUCCESS(f'PDF generated at: {temp_path}'))
        except PermissionError:
            self.stdout.write(self.style.ERROR(f'Permission denied: Unable to write PDF to {temp_path}. Please check file permissions or try running with elevated privileges.'))
