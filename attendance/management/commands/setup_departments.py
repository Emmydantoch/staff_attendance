from django.core.management.base import BaseCommand
from attendance.models import Department

# This Python class creates initial departments for a system by populating a list of department names
# and descriptions in a Django model.
class Command(BaseCommand):
    help = 'Create initial departments for the system'

    def handle(self, *args, **options):
        departments = [
            {"name": "Human Resources Team", "description": "Handles recruitment, employee relations, and benefits"},
            {"name": "Software Development Team", "description": "Responsible for developing and maintaining software products"},
            {"name": "Finance & Accounting Team", "description": "Handles accounting, budgeting, and financial planning"},
            {"name": "Community Management Team", "description": "Focuses on building and managing community relationships"},
            {"name": "Marketing Team", "description": "Manages brand, advertising, and promotions"},
            {"name": "Sales Team", "description": "Handles customer acquisition and revenue generation"},
            {"name": "Creative Media Team", "description": "Focuses on content creation and branding"},
            {"name": "Product Management Team", "description": "Oversees product development and lifecycle management"},
            {"name": "Design UI/UX Team", "description": "Responsible for product design and user experience"},
            {"name": "Data Management Team", "description": "Oversees data governance and analytics"},
            {"name": "Trainee ", "description": "They are trainees who have payed for a particular course"},
            {"name": "IT_student ", "description": " They are students taking IT related courses"},
            {"name": "Intern", "description": " They are interns working in various departments under agreements"},
            {"name": "Ideas/3mtt", "description": "they students taking sponsoured courses"},
        ]

        created_count = 0
        for dept in departments:
            _, created = Department.objects.get_or_create(
                name=dept["name"],
                defaults={"description": dept["description"]}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created department: {dept["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} departments'))
