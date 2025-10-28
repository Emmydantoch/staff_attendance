from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", lambda request: redirect("dashboard"), name="home"),
    path("register/", views.register, name="register"),
    path("sign-in-out/", views.sign_in_out, name="sign_in_out"),
    path("attendance/", views.attendance_list, name="attendance_list"),
    path(
        "export/<str:format_type>/", views.export_attendance, name="export_attendance"
    ),
    path("leave-request/", views.leave_request, name="leave_request"),
    path(
        "attendance/save-note/", views.save_attendance_note, name="save_attendance_note"
    ),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "dashboard/chart-data/",
        views.attendance_chart_data,
        name="attendance_chart_data",
    ),
    path("all-time-off/", views.all_time_off, name="all_time_off"),
    path(
        "leave-request/<int:leave_id>/approve/",
        views.approve_leave_request,
        name="approve_leave_request",
    ),
    path(
        "leave-request/<int:leave_id>/reject/",
        views.reject_leave_request,
        name="reject_leave_request",
    ),
    # Profile URL
    path("profile/", views.profile, name="profile"),
    # Barcode/QR Code URLs
    path("my-barcode/", views.my_barcode, name="my_barcode"),
    path("barcode-scan/", views.barcode_scan_page, name="barcode_scan_page"),
    path("barcode-authenticate/", views.barcode_authenticate, name="barcode_authenticate"),
    # Todo List URLs
    path("todos/", views.get_todos, name="get_todos"),
    path("todos/create/", views.create_todo, name="create_todo"),
    path("todos/<int:todo_id>/update-status/", views.update_todo_status, name="update_todo_status"),
    path("todos/<int:todo_id>/delete/", views.delete_todo, name="delete_todo"),
    # Staff API
    path("api/staff-members/", views.get_staff_members, name="get_staff_members"),
    # Delegated Duty URLs
    path("duties/create/", views.create_delegated_duty, name="create_delegated_duty"),
    path("duties/", views.get_delegated_duties, name="get_delegated_duties"),
]
