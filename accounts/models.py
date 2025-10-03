from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default User model with additional fields.
    """

    # Additional fields
    phone = models.CharField(
        _("phone number"),
        max_length=15,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message=_(
                    "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
                ),
            )
        ],
        help_text=_("Format: +1234567890"),
    )

    # Department information
    department = models.ForeignKey(
        "attendance.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="staff_members",
        verbose_name=_("department"),
    )

    # Employment information
    hire_date = models.DateField(
        _("hire date"),
        default=timezone.now,
        help_text=_("Date when the employee was hired"),
    )

    position = models.CharField(
        _("position"), max_length=100, blank=True, help_text=_("Job position or title")
    )

    bio = models.TextField(
        _("bio"), blank=True, help_text=_("A short bio or description")
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )

    # Profile picture
    profile_picture = models.ImageField(
        _("profile picture"),
        upload_to="profile_pics/",
        blank=True,
        null=True,
        help_text=_("Upload a profile picture (optional)"),
    )

    # Timestamps
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_updated = models.DateTimeField(_("last updated"), auto_now=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def full_name(self):
        """Return the full name of the user."""
        return self.get_full_name()
