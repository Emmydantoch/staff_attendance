from django.contrib import admin
from .models import Department, Staff, Attendance, LeaveRequest, TodoItem, DelegatedDuty


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
    list_display = ("user", "date", "sign_in", "sign_out", "location", "notes")
    search_fields = ("user__username", "user__first_name", "user__last_name", "date", "location")
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


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "title",
        "status",
        "created_at",
        "started_at",
        "completed_at",
    )
    search_fields = ("user__username", "user__first_name", "user__last_name", "title")
    list_filter = ("status", "created_at", "user")
    readonly_fields = ("created_at", "updated_at")


@admin.register(DelegatedDuty)
class DelegatedDutyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "assigned_to",
        "assigned_by",
        "priority",
        "due_date",
        "status",
        "created_at",
    )
    search_fields = (
        "title",
        "assigned_to__username",
        "assigned_to__first_name",
        "assigned_to__last_name",
        "assigned_by__username",
    )
    list_filter = ("status", "priority", "due_date", "created_at")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ["assigned_to", "assigned_by"]
