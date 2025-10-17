from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import uuid


class Department(models.Model):
    """Department model to categorize staff members"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Staff(models.Model):
    """Staff model extending the default User model"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_profile"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="staff_department_members",  # changed to avoid conflict
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        help_text="Format: +1234567890",
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
    )
    hire_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    position = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True, help_text="A short bio or description")

    # Profile picture
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True,
        help_text="Upload a profile picture (optional)",
    )
    
    # Barcode for authentication
    barcode = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        help_text="Unique barcode/QR code for staff authentication"
    )

    def save(self, *args, **kwargs):
        # Generate unique barcode if not exists
        if not self.barcode:
            self.barcode = f"STAFF-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Attendance(models.Model):
    """
    Model to track staff attendance with sign-in and sign-out times.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        null=True,
        blank=True,
    )
    sign_in = models.DateTimeField(
        _("sign in time"), null=True, blank=True, help_text=_("When the user signed in")
    )
    sign_out = models.DateTimeField(
        _("sign out time"),
        null=True,
        blank=True,
        help_text=_("When the user signed out"),
    )
    date = models.DateField(
        _("date"), auto_now_add=True, help_text=_("The date of the attendance record")
    )
    notes = models.TextField(
        _("notes"),
        blank=True,
        help_text=_("Any additional notes about this attendance record"),
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        help_text=_("When this record was created"),
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(
        _("updated at"), auto_now=True, help_text=_("When this record was last updated")
    )

    class Meta:
        verbose_name = _("attendance record")
        verbose_name_plural = _("attendance records")
        ordering = ["-date", "-sign_in"]
        unique_together = ("user", "date")  # One record per user per day
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["date"]),
            models.Index(fields=["sign_in"]),
            models.Index(fields=["sign_out"]),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.date}"

    @property
    def duration(self):
        """
        Calculate the duration between sign in and sign out.
        Returns None if either time is not set.
        """
        if self.sign_in and self.sign_out:
            return self.sign_out - self.sign_in
        return None

    def is_signed_in(self):
        """Check if the user is currently signed in (signed in but not out)."""
        return bool(self.sign_in and not self.sign_out)


class LeaveRequest(models.Model):
    """
    Model to track staff leave requests.
    """

    REQUEST_TYPE_CHOICES = [
        ("Leave", _("Leave")),
        ("Suggestion_box", _("Suggestion_box")),
        ("Remote Work", _("Remote Work")),
    ]
    STATUS_CHOICES = [
        ("Pending", _("Pending")),
        ("Approved", _("Approved")),
        ("Rejected", _("Rejected")),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leave_requests",
        verbose_name=_("user"),
        null=True,
        blank=True,
    )
    type = models.CharField(
        _("Request Type"),
        max_length=20,
        choices=REQUEST_TYPE_CHOICES,
        default="Leave",
        help_text=_("Type of request: Leave or Remote Work"),
    )
    start_date = models.DateField(
        _("start date"), help_text=_("First day of leave"), null=True, blank=True
    )
    end_date = models.DateField(
        _("end date"), help_text=_("Last day of leave"), null=True, blank=True
    )
    reason = models.TextField(_("reason"), help_text=_("Reason for leave"))
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
        help_text=_("Current status of the leave request"),
    )
    created_at = models.DateTimeField(
        _("created at"), auto_now_add=True, help_text=_("When this request was created")
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        help_text=_("When this request was last updated"),
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_leave_requests",
        verbose_name=_("reviewed by"),
        help_text=_("Admin who reviewed this request"),
    )
    review_notes = models.TextField(
        _("review notes"), blank=True, help_text=_("Notes from the reviewer")
    )

    class Meta:
        verbose_name = _("leave request")
        verbose_name_plural = _("leave requests")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "start_date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["start_date", "end_date"]),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.start_date} to {self.end_date} ({self.status})"

    @property
    def duration(self):
        """Calculate the duration of the leave in days."""
        return (
            self.end_date - self.start_date
        ).days + 1  # +1 to include both start and end dates

    def is_approved(self):
        """Check if the leave request is approved."""
        return self.status == "Approved"

    def is_pending(self):
        """Check if the leave request is pending review."""
        return self.status == "Pending"


# Create your models here.
