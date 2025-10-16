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
]
