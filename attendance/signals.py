from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Staff

User = get_user_model()


@receiver(post_save, sender=User)
def create_staff_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Staff profile when a new user is created.
    """
    if created:
        # Use get_or_create to prevent duplicate creation
        try:
            Staff.objects.get_or_create(
                user=instance,
                defaults={
                    'department': instance.department if hasattr(instance, 'department') else None,
                    'phone': instance.phone if hasattr(instance, 'phone') else '',
                    'position': instance.position if hasattr(instance, 'position') else '',
                    'bio': instance.bio if hasattr(instance, 'bio') else '',
                    'is_active': instance.is_active
                }
            )
        except Exception as e:
            # Log the error but don't crash
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error creating Staff profile for {instance.username}: {str(e)}")
