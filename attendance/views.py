from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.http import JsonResponse


# List all time off requests for the current user (or all for admin)
@login_required
def all_time_off(request):
    if request.user.is_staff:
        all_time_off = LeaveRequest.objects.all().order_by("-created_at")
    else:
        all_time_off = LeaveRequest.objects.filter(user=request.user).order_by(
            "-created_at"
        )
    context = {
        "all_time_off": all_time_off,
        "is_staff": request.user.is_staff,
    }
    return render(request, "all_time_off.html", context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login, authenticate
from .models import Department, Attendance, LeaveRequest
from .forms import StaffRegistrationForm, SignInOutForm, LeaveRequestForm

# removed import of CustomUser
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from datetime import timedelta
import logging
import json

logger = logging.getLogger(__name__)


def register(request):
    """
    Handle user registration with the custom user model.
    """
    from .models import Staff
    
    if request.user.is_authenticated:
        messages.info(request, _("You are already logged in."))
        return redirect("dashboard")

    if request.method == "POST":
        form = StaffRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save the user with the form data
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password1"])
                user.save()

                # Create Staff profile for the user (if not already created by signal)
                staff, created = Staff.objects.get_or_create(
                    user=user,
                    defaults={
                        'department': user.department if hasattr(user, 'department') else None,
                        'phone': user.phone if hasattr(user, 'phone') else '',
                        'position': user.position if hasattr(user, 'position') else '',
                        'bio': user.bio if hasattr(user, 'bio') else '',
                        'is_active': True
                    }
                )

                # Log the successful registration
                logger.info(f"New user registered: {user.username} ({user.email})")

                # Authenticate and log the user in
                user = authenticate(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password1"],
                )

                if user is not None:
                    login(request, user)
                    messages.success(
                        request, _("Registration successful! You are now logged in.")
                    )
                    return redirect("dashboard")
                else:
                    messages.success(
                        request,
                        _(
                            "Registration successful! Please log in with your credentials."
                        ),
                    )
                    return redirect("login")

            except Exception as e:
                logger.error(f"Error during registration: {str(e)}", exc_info=True)
                messages.error(
                    request,
                    _("An error occurred during registration. Please try again."),
                )
    else:
        form = StaffRegistrationForm()

    return render(request, "register.html", {"form": form})


@login_required
def sign_in_out(request):
    """
    Handle staff sign in/out functionality.
    """
    user = request.user
    today = timezone.now().date()

    # Get or create attendance record for today
    attendance, created = Attendance.objects.get_or_create(
        user=user, date=today, defaults={"sign_in": timezone.now()}
    )

    status_message = None
    show_form = True
    show_sign_in = False
    show_sign_out = False
    sign_time = None

    if request.method == "POST":
        form = SignInOutForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data["action"]
            if action == "sign_in" and not attendance.sign_in:
                attendance.sign_in = timezone.now()
                attendance.save()
                request.session["status_message"] = (
                    "You signed in successfully today. Welcome! we wish you a productive day ahead."
                )
                request.session["sign_time"] = str(attendance.sign_in)
                return redirect("sign_in_out")
            elif (
                action == "sign_out" and attendance.sign_in and not attendance.sign_out
            ):
                attendance.sign_out = timezone.now()
                attendance.save()
                request.session["status_message"] = (
                    "You signed out successfully. Goodbye!"
                )
                # Ask user to leave a note after signing out
                request.session["prompt_attendance_note"] = attendance.id
                request.session["sign_time"] = str(attendance.sign_out)
                return redirect("sign_in_out")
            else:
                request.session["status_message"] = (
                    "Invalid action or already signed in/out."
                )
                return redirect("sign_in_out")
    else:
        form = SignInOutForm()

    # Get status message from session if available
    if "status_message" in request.session:
        status_message = request.session.pop("status_message")
        sign_time = request.session.pop("sign_time", None)
    # Pop the prompt flag for attendance note (if set) so template can show modal
    prompt_attendance_note = request.session.pop("prompt_attendance_note", None)

    # Control which button/form to show
    if not attendance.sign_in:
        show_sign_in = True
    elif attendance.sign_in and not attendance.sign_out:
        show_sign_out = True
    else:
        show_form = False

    return render(
        request,
        "sign_in_out.html",
        {
            "form": form,
            "attendance": attendance,
            "show_form": show_form,
            "show_sign_in": show_sign_in,
            "show_sign_out": show_sign_out,
            "status_message": status_message,
            "sign_time": sign_time,
            "prompt_attendance_note": prompt_attendance_note,
        },
    )


@login_required
def attendance_list(request):
    if not request.user.is_staff:
        return redirect("sign_in_out")

    attendances = Attendance.objects.all()
    if request.GET.get("user"):
        attendances = attendances.filter(user__username=request.GET["user"])
    if request.GET.get("date"):
        attendances = attendances.filter(date=request.GET["date"])

    return render(request, "attendance_list.html", {"attendances": attendances})


@login_required
def save_attendance_note(request):
    """AJAX endpoint to save a note for an attendance record."""
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            attendance_id = data.get("attendance_id")
            note = data.get("note", "").strip()
            att = Attendance.objects.get(id=attendance_id, user=request.user)
            att.notes = note
            att.save()
            return JsonResponse({"status": "ok"})
        except Attendance.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Attendance not found"}, status=404
            )
        except Exception as e:
            logger.exception("Error saving attendance note")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)


@login_required
def export_attendance(request, format_type):
    if not request.user.is_staff:
        return redirect("sign_in_out")

    attendances = Attendance.objects.all()
    data = [
        {
            "User": str(att.user),
            "Date": att.date,
            "Sign In": att.sign_in,
            "Sign Out": att.sign_out,
            "Notes": att.notes,
        }
        for att in attendances
    ]

    if format_type == "csv":
        df = pd.DataFrame(data)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="attendance.csv"'
        df.to_csv(response, index=False)
        return response
    elif format_type == "excel":
        df = pd.DataFrame(data)
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="attendance.xlsx"'
        df.to_excel(response, index=False)
        return response
    elif format_type == "pdf":
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="attendance.pdf"'
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        y = 750
        for item in data:
            p.drawString(
                50,
                y,
                f"User: {item['User']}, Date: {item['Date']}, Sign In: {item['Sign In']}, Sign Out: {item['Sign Out']}",
            )
            y -= 20
            if y < 50:
                p.showPage()
                y = 750
        p.save()
        buffer.seek(0)
        response.write(buffer.getvalue())
        buffer.close()
        return response


@login_required
def leave_request(request):
    if request.method == "POST":
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            messages.success(request, "request submitted.")
            return redirect("sign_in_out")
    else:
        form = LeaveRequestForm()
    return render(request, "leave_request.html", {"form": form})


import logging

logger = logging.getLogger(__name__)


@login_required
def dashboard(request):
    try:
        logger.info(
            f"Dashboard accessed by {request.user.username} (staff: {request.user.is_staff})"
        )

        staff_profile = getattr(request.user, "staff", None)
        today = timezone.now().date()
        now = timezone.now()
        month_start = today.replace(day=1)
        late_threshold = now.replace(hour=9, minute=0, second=0, microsecond=0).time()

        # Days worked this month (distinct days with sign_in)
        days_worked = Attendance.objects.filter(
            user=request.user,
            sign_in__isnull=False,
            date__gte=month_start,
            date__lte=today,
        ).count()

        # Calculate percentage of days worked (assuming 22 working days per month)
        days_worked_percent = (
            min(int((days_worked / 22) * 100), 100) if days_worked else 0
        )

        # Late arrivals this month
        late_arrivals = Attendance.objects.filter(
            user=request.user,
            sign_in__isnull=False,
            sign_in__time__gt=late_threshold,
            date__gte=month_start,
            date__lte=today,
        ).count()

        # Recent attendance/activity (last 5 records)
        recent_attendance_qs = Attendance.objects.filter(user=request.user).order_by(
            "-date", "-sign_in"
        )[:5]
        recent_attendance = []
        for att in recent_attendance_qs:
            duration_str = "--:--"
            if att.sign_in and att.sign_out:
                delta = att.sign_out - att.sign_in
                total_seconds = int(delta.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                duration_str = f"{hours}:{minutes:02d}"
            # Attach as a template-safe attribute (no underscore)
            att.duration_str = duration_str
            recent_attendance.append(att)

        # Recent leave requests
        if request.user.is_staff:
            # Admin sees all recent leave/remote work requests (last 10)
            recent_leaves = LeaveRequest.objects.all().order_by("-created_at")[:10]
        else:
            # User sees their own recent leave/remote work requests (last 5)
            recent_leaves = LeaveRequest.objects.filter(user=request.user).order_by(
                "-created_at"
            )[:5]

        # Upcoming time off (future leave requests, approved or pending)
        upcoming_time_off = LeaveRequest.objects.filter(
            user=request.user, end_date__gte=today, status__in=["Approved", "Pending"]
        ).order_by("start_date")

        # Add days attribute to each leave object for template access
        for leave in upcoming_time_off:
            leave.days = leave.duration

        # Remaining vacation days (example: assume 20 per year minus approved leaves)
        approved_leaves = LeaveRequest.objects.filter(
            user=request.user, status="Approved", start_date__year=today.year
        )
        days_taken = sum(
            [(leave.end_date - leave.start_date).days + 1 for leave in approved_leaves]
        )
        vacation_days_total = 20
        vacation_days_left = max(vacation_days_total - days_taken, 0)

        # Staff-specific data
        late_attendances = []
        date_strs = []
        late_counts = []
        pending_leaves = 0
        active_employees = 0
        on_time_percent = 0
        if request.user.is_staff:
            # Today's late attendances (all users)
            late_attendances = Attendance.objects.filter(
                date=today, sign_in__time__gt=late_threshold
            )
            # Chart: late sign-ins per day for last 7 days
            end_date = today
            start_date = end_date - timedelta(days=6)
            date_range = [start_date + timedelta(days=x) for x in range(7)]
            for date in date_range:
                count = Attendance.objects.filter(
                    date=date, sign_in__time__gt=late_threshold
                ).count()
                date_strs.append(date.strftime("%Y-%m-%d"))
                late_counts.append(count)
            # Pending leave requests
            pending_leaves = LeaveRequest.objects.filter(status="Pending").count()
            # Active employees (users with attendance in last 30 days)
            active_employees = (
                Attendance.objects.filter(date__gte=today - timedelta(days=30))
                .values("user")
                .distinct()
                .count()
            )
            # On-time attendance percent (today)
            total_today = Attendance.objects.filter(date=today).count()
            on_time_today = Attendance.objects.filter(
                date=today, sign_in__isnull=False, sign_in__time__lte=late_threshold
            ).count()
            on_time_percent = (
                int((on_time_today / total_today) * 100) if total_today else 0
            )

        # Prefer position from CustomUser, fallback to staff_profile if needed
        user_role = getattr(request.user, "position", None)
        if not user_role:
            user_role = getattr(staff_profile, "position", "") if staff_profile else ""
        user_role = user_role.strip() if user_role else ""

        # Get the user's department
        department = None
        if hasattr(request.user, "department") and request.user.department:
            department = request.user.department.name

        context = {
            "user": request.user,
            "is_staff": request.user.is_staff,
            "staff_profile": staff_profile,
            "days_worked": days_worked,
            "days_worked_percent": days_worked_percent,
            "late_arrivals": late_arrivals,
            "recent_attendance": recent_attendance,
            "recent_user_attendance": recent_attendance,  # For employee dashboard
            "recent_leaves": recent_leaves,
            "upcoming_time_off": upcoming_time_off,
            "vacation_days_left": vacation_days_left,
            "vacation_days_total": vacation_days_total,
            "user_role": user_role,
            "department": department,
        }
        if request.user.is_staff:
            context.update(
                {
                    "late_count": len(late_attendances),
                    "chart_labels": json.dumps(date_strs),
                    "chart_data": json.dumps(late_counts),
                    "pending_leaves": pending_leaves,
                    "active_employees": active_employees,
                    "on_time_percent": on_time_percent,
                }
            )
        return render(request, "dashboard.html", context)
    except Exception as e:
        logger.error(f"Error in dashboard view: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while loading the dashboard.")
        return redirect("home")


@login_required
def attendance_chart_data(request):
    """Return JSON with labels and data for the last 7 days late arrivals (admin only)."""
    if not request.user.is_staff:
        return JsonResponse({"error": "forbidden"}, status=403)

    try:
        today = timezone.now().date()
        end_date = today
        start_date = end_date - timedelta(days=6)
        date_range = [start_date + timedelta(days=x) for x in range(7)]
        labels = [d.strftime("%Y-%m-%d") for d in date_range]
        late_threshold = (
            timezone.now().replace(hour=9, minute=0, second=0, microsecond=0).time()
        )
        data = [
            Attendance.objects.filter(date=d, sign_in__time__gt=late_threshold).count()
            for d in date_range
        ]
        return JsonResponse({"labels": labels, "data": data})
    except Exception as e:
        logger.error(f"Error generating chart data: {e}", exc_info=True)
        return JsonResponse({"error": "internal"}, status=500)


# Create your views here.
# Admin action to approve/reject leave requests from dashboard
@login_required
@require_POST
def approve_leave_request(request, leave_id):
    if not request.user.is_staff:
        return redirect("dashboard")
    leave = LeaveRequest.objects.get(id=leave_id)
    leave.status = "Approved"
    leave.reviewed_by = request.user
    leave.save()
    messages.success(
        request,
        f"Leave request for {leave.user.get_full_name() or leave.user.username} approved.",
    )
    return redirect("dashboard")


@login_required
@require_POST
def reject_leave_request(request, leave_id):
    if not request.user.is_staff:
        return redirect("dashboard")
    leave = LeaveRequest.objects.get(id=leave_id)
    leave.status = "Rejected"
    leave.reviewed_by = request.user
    leave.save()
    messages.success(
        request,
        f"Leave request for {leave.user.get_full_name() or leave.user.username} rejected.",
    )
    return redirect("dashboard")


# Barcode/QR Code Views
@login_required
def my_barcode(request):
    """Display the user's barcode/QR code for scanning"""
    from .models import Staff
    try:
        staff = Staff.objects.get(user=request.user)
        return render(request, "my_barcode.html", {"staff": staff})
    except Staff.DoesNotExist:
        messages.error(request, "Staff profile not found. Please contact admin.")
        return redirect("dashboard")


def barcode_scan_page(request):
    """Page for scanning barcodes to sign in/out"""
    return render(request, "barcode_scan.html")


@require_POST
def barcode_authenticate(request):
    """Authenticate user via barcode and perform sign in/out"""
    from .models import Staff
    
    try:
        data = json.loads(request.body)
        barcode = data.get("barcode", "").strip()
        
        if not barcode:
            return JsonResponse({"success": False, "message": "No barcode provided"}, status=400)
        
        # Find staff by barcode
        try:
            staff = Staff.objects.get(barcode=barcode)
            user = staff.user
        except Staff.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid barcode"}, status=404)
        
        # Check if user is active
        if not staff.is_active:
            return JsonResponse({"success": False, "message": "Staff account is inactive"}, status=403)
        
        # Get or create attendance for today
        today = timezone.now().date()
        attendance, created = Attendance.objects.get_or_create(
            user=user, date=today, defaults={"sign_in": timezone.now()}
        )
        
        # Determine action: sign in or sign out
        if not attendance.sign_in:
            attendance.sign_in = timezone.now()
            attendance.save()
            return JsonResponse({
                "success": True,
                "action": "sign_in",
                "message": f"Welcome {user.get_full_name() or user.username}! You signed in successfully.",
                "time": attendance.sign_in.strftime("%H:%M:%S"),
                "user": user.get_full_name() or user.username
            })
        elif attendance.sign_in and not attendance.sign_out:
            attendance.sign_out = timezone.now()
            attendance.save()
            return JsonResponse({
                "success": True,
                "action": "sign_out",
                "message": f"Goodbye {user.get_full_name() or user.username}! You signed out successfully.",
                "time": attendance.sign_out.strftime("%H:%M:%S"),
                "user": user.get_full_name() or user.username
            })
        else:
            return JsonResponse({
                "success": False,
                "message": "You have already completed sign in/out for today."
            })
            
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid request data"}, status=400)
    except Exception as e:
        logger.error(f"Error in barcode authentication: {str(e)}", exc_info=True)
        return JsonResponse({"success": False, "message": "An error occurred"}, status=500)
