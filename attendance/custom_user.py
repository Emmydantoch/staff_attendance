from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string

class CustomUser(AbstractUser):
    """
    Custom user model that extends the default User model with additional fields.
    """
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(
        _('phone number'),
        max_length=15,
        blank=True,
        help_text=_('Format: +1234567890')
    )
    
    # Email verification fields
    email_verified = models.BooleanField(
        _('email verified'),
        default=False,
        help_text=_('Designates whether this user has verified their email address.')
    )
    email_verification_token = models.CharField(
        _('email verification token'),
        max_length=64,
        blank=True,
        null=True,
        help_text=_('Token used for email verification')
    )
    email_token_created = models.DateTimeField(
        _('token created at'),
        null=True,
        blank=True,
        help_text=_('When the verification token was created')
    )
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email
    
    def generate_verification_token(self):
        """Generate a unique verification token"""
        self.email_verification_token = get_random_string(64)
        from django.utils import timezone
        self.email_token_created = timezone.now()
        self.save()
        return self.email_verification_token
