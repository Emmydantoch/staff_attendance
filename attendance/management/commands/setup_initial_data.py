from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from attendance.models import Department

class Command(BaseCommand):
    help = 'Creates initial departments for the application'

    def handle(self, *args, **options):
        departments = [
            {
                'name': 'Human Resources',
                'description': _('Handles recruitment, employee relations, and benefits')
            },
            {
                'name': 'Information Technology',
                'description': _('Manages technology infrastructure and support')
            },
            {
                'name': 'Finance',
                'description': _('Handles accounting, budgeting, and financial planning')
            },
            {
                'name': 'Marketing',
                'description': _('Manages brand, advertising, and market research')
            },
            {
                'name': 'Operations',
                'description': _('Oversees daily business activities and processes')
            },
            {
                'name': 'Sales',
                'description': _('Handles customer acquisition and revenue generation')
            },
            {
                'name': 'Customer Support',
                'description': _('Provides assistance to customers and resolves issues')
            },
            {
                'name': 'Research and Development',
                'description': _('Focuses on innovation and product development')
            },
            {
                'name': 'Administration',
                'description': _('Manages office operations and administrative tasks')
            },
            {
                'name': 'Executive',
                'description': _('Senior leadership and strategic decision-making')
            }
        ]

        created_count = 0
        for dept in departments:
            obj, created = Department.objects.get_or_create(
                name=dept['name'],
                defaults={'description': dept['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created department: {dept["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Department already exists: {dept["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} departments'))
