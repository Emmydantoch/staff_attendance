from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .models import Department, LeaveRequest
from accounts.models import CustomUser

# removed import of CustomUser


class StaffRegistrationForm(UserCreationForm):
    """Form for user registration with extended fields."""

    # Required fields
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("First name"),
                "autofocus": True,
            }
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Last name")}
        ),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("Email address")}
        ),
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message=_(
                    "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
                ),
            )
        ],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("e.g. +1234567890"),
                "pattern": r"^\+?1?\d{9,15}$",
            }
        ),
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        empty_label=_("Select Department"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "phone", "department")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Choose a username"),
                    "autocomplete": "username",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update widget attributes for password fields
        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": _("Create a password"),
                "autocomplete": "new-password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": _("Confirm password"),
                "autocomplete": "new-password",
            }
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # If you want to check for unique email, use the AUTH_USER_MODEL
        # from django.contrib.auth import get_user_model
        # User = get_user_model()
        # if User.objects.filter(email=email).exists():
        #     raise forms.ValidationError(_("This email is already in use. Please use a different email."))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone = self.cleaned_data["phone"]
        user.is_active = True  # Ensure user is always active on registration
        if commit:
            user.save()
            # No need to create a separate Staff object as we're using CustomUser (removed)
        return user


class SignInOutForm(forms.Form):
    action = forms.ChoiceField(
        choices=[("sign_in", "Sign In"), ("sign_out", "Sign Out")]
    )


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ["type", "start_date", "end_date", "reason"]
        widgets = {
            "type": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make start_date and end_date optional so 'Suggestion' requests don't require them
        self.fields["start_date"].required = False
        self.fields["end_date"].required = False
