from django.core.management.base import BaseCommand
from biodata.models import CandidateBiodata
from django.db.models import Count

class Command(BaseCommand):
    help = 'Find duplicate and NULL registrant_mobile values in CandidateBiodata'

    def handle(self, *args, **options):
        # Find duplicates
        duplicates = CandidateBiodata.objects.values('registrant_mobile')\
            .annotate(count=Count('registrant_mobile'))\
            .filter(count__gt=1)\
            .exclude(registrant_mobile__isnull=True)\
            .order_by('registrant_mobile')

        if duplicates:
            self.stdout.write("Duplicate registrant_mobile values:")
            for dup in duplicates:
                self.stdout.write(f"Value: {dup['registrant_mobile']} - Count: {dup['count']}")
                records = CandidateBiodata.objects.filter(registrant_mobile=dup['registrant_mobile'])
                for rec in records:
                    self.stdout.write(f"  ID: {rec.id}, Candidate Name: {rec.candidate_name}")
        else:
            self.stdout.write("No duplicate registrant_mobile values found.")

        # Find NULL or empty registrant_mobile
        nulls = CandidateBiodata.objects.filter(registrant_mobile__isnull=True)
        if nulls.exists():
            self.stdout.write("\nRecords with NULL registrant_mobile:")
            for rec in nulls:
                self.stdout.write(f"ID: {rec.id}, Candidate Name: {rec.candidate_name}")
        else:
            self.stdout.write("\nNo records with NULL registrant_mobile found.")
