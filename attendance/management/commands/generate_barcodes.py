from django.core.management.base import BaseCommand
from attendance.models import Staff
import uuid


class Command(BaseCommand):
    help = 'Generate barcodes for staff members who do not have one'

    def handle(self, *args, **options):
        staff_without_barcode = Staff.objects.filter(barcode='')
        count = 0
        
        for staff in staff_without_barcode:
            staff.barcode = f"STAFF-{uuid.uuid4().hex[:12].upper()}"
            staff.save()
            count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'Generated barcode for {staff.user.get_full_name() or staff.user.username}: {staff.barcode}'
                )
            )
        
        if count == 0:
            self.stdout.write(self.style.WARNING('All staff members already have barcodes'))
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully generated {count} barcodes')
            )
