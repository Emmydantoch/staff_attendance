import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'staff_attendance.settings')
django.setup()

from attendance.models import Attendance

# Sample location (Kinplus Technologies)
kinplus_location = "Kinplus Technologies, 2nd floor, 68B Christore Building, Hospital Road, Opp. Ekiti State University Teaching Hospital, Ekiti State, Nigeria"

# Update recent records with sample location
records = Attendance.objects.filter(location='').order_by('-id')[:5]
updated_count = 0

for record in records:
    record.location = kinplus_location
    record.save()
    updated_count += 1
    print(f"Updated: {record.user.username} - {record.date}")

print(f"\nTotal updated: {updated_count} records")
