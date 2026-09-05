"""
URL configuration for OurProject project.
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [

    # Django Admin
    path(
        "admin/",
        admin.site.urls
    ),

    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Authentication
    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # Citizen Dashboard
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    # Create Complaint
    path(
        "complaint/new/",
        views.create_complaint,
        name="create_complaint"
    ),

    # Complaint Detail
    path(
        "complaint/<int:complaint_id>/",
        views.complaint_detail,
        name="complaint_detail"
    ),

    # Admin Dashboard
    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    # Registered Citizens
    path(
        "admin-dashboard/citizens/",
        views.registered_citizens,
        name="registered_citizens"
    ),

    # All Complaints
    path(
        "admin-dashboard/complaints/",
        views.all_complaints,
        name="all_complaints"
    ),

   


]


# Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )