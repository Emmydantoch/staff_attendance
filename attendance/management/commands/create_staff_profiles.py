from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from attendance.models import Staff

User = get_user_model()


class Command(BaseCommand):
    help = 'Create Staff profiles for users who do not have one'

    def handle(self, *args, **options):
        users_without_staff = User.objects.filter(staff_profile__isnull=True)
        count = 0
        
        for user in users_without_staff:
            staff = Staff.objects.create(
                user=user,
                department=user.department if hasattr(user, 'department') else None,
                phone=user.phone if hasattr(user, 'phone') else '',
                position=user.position if hasattr(user, 'position') else '',
                bio=user.bio if hasattr(user, 'bio') else '',
                is_active=user.is_active
            )
            count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created Staff profile for {user.get_full_name() or user.username} (Barcode: {staff.barcode})'
                )
            )
        
        if count == 0:
            self.stdout.write(self.style.WARNING('All users already have Staff profiles'))
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {count} Staff profiles')
            )
