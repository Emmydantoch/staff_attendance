from django.utils import timezone
from .models import Attendance


def attendance_status(request):
    """
    Context processor to provide the current user's attendance status
    to all templates.
    """
    context = {
        'user_signed_in_today': False,
        'user_signed_out_today': False,
        'show_sign_in': True,
        'show_sign_out': False,
    }
    
    if request.user.is_authenticated:
        today = timezone.now().date()
        try:
            attendance = Attendance.objects.get(user=request.user, date=today)
            
            # User has an attendance record for today
            if attendance.sign_in and not attendance.sign_out:
                # User is signed in but not signed out
                context['user_signed_in_today'] = True
                context['show_sign_in'] = False
                context['show_sign_out'] = True
            elif attendance.sign_out:
                # User has signed out
                context['user_signed_out_today'] = True
                context['show_sign_in'] = False
                context['show_sign_out'] = False
            # If neither sign_in nor sign_out, show sign in (default)
            
        except Attendance.DoesNotExist:
            # No attendance record for today, show sign in (default)
            pass
    
    return context
