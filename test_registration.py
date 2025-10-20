"""
Quick test script to verify registration works
Run with: python manage.py shell < test_registration.py
"""

from django.contrib.auth import get_user_model
from attendance.models import Staff, Department

User = get_user_model()

# Create a test department if it doesn't exist
dept, _ = Department.objects.get_or_create(
    name="Test Department",
    defaults={"description": "Test department for registration"}
)

# Test user data
test_username = "testuser123"
test_email = "testuser123@example.com"

# Clean up if test user already exists
User.objects.filter(username=test_username).delete()

print("Creating test user...")

# Create user
user = User.objects.create_user(
    username=test_username,
    email=test_email,
    password="testpass123",
    first_name="Test",
    last_name="User",
    phone="+1234567890",
    department=dept
)

print(f"✅ User created: {user.username}")

# Check if Staff profile was created by signal
try:
    staff = Staff.objects.get(user=user)
    print(f"✅ Staff profile created automatically!")
    print(f"   - Barcode: {staff.barcode}")
    print(f"   - Department: {staff.department}")
    print(f"   - Phone: {staff.phone}")
    print(f"   - Active: {staff.is_active}")
except Staff.DoesNotExist:
    print("❌ Staff profile NOT created - signal may not be working")

# Clean up
print("\nCleaning up test data...")
user.delete()
print("✅ Test complete!")
