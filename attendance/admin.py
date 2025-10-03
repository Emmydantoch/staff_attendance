from django.contrib import admin
from .models import Department, Staff, Attendance, LeaveRequest


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "phone", "hire_date", "is_active", "position")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "department__name",
    )
    list_filter = ("department", "is_active")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "sign_in", "sign_out", "notes")
    search_fields = ("user__username", "user__first_name", "user__last_name", "date")
    list_filter = ("date", "user")


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "start_date",
        "end_date",
        "status",
        "created_at",
        "reviewed_by",
    )
    search_fields = ("user__username", "user__first_name", "user__last_name", "status")
    list_filter = ("status", "created_at", "user")

    actions = ["approve_selected", "reject_selected"]

    def approve_selected(self, request, queryset):
        updated = queryset.update(status="Approved", reviewed_by=request.user)
        self.message_user(request, f"{updated} leave request(s) approved.")

    approve_selected.short_description = "Approve selected leave requests"

    def reject_selected(self, request, queryset):
        updated = queryset.update(status="Rejected", reviewed_by=request.user)
        self.message_user(request, f"{updated} leave request(s) rejected.")

    reject_selected.short_description = "Reject selected leave requests"
