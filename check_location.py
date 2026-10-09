import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'staff_attendance.settings')
django.setup()

from attendance.models import Attendance

print("Checking attendance records for location data:")
print("-" * 80)

records = Attendance.objects.all().order_by('-id')[:10]
for r in records:
    location_display = r.location if r.location else "(empty)"
    print(f"ID: {r.id} | User: {r.user.username} | Date: {r.date} | Location: {location_display}")

print("-" * 80)
print(f"Total records: {Attendance.objects.count()}")
print(f"Records with location: {Attendance.objects.exclude(location='').exclude(location__isnull=True).count()}")
