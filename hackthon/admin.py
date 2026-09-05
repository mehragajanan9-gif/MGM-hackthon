from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Profile, Complaint


# ==========================
# USER ADMIN
# ==========================

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "get_phone",
        "get_role",
        "is_active",
        "date_joined",
    )

    search_fields = (
        "username",
        "email",
    )

    def get_phone(self, obj):

        try:
            return obj.profile.phone
        except Profile.DoesNotExist:
            return "-"

    get_phone.short_description = "Phone"

    def get_role(self, obj):

        try:
            return obj.profile.role
        except Profile.DoesNotExist:
            return "-"

    get_role.short_description = "Role"


# ==========================
# PROFILE ADMIN
# ==========================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "role",
        "phone",
    )

    list_filter = (
        "role",
    )

    search_fields = (
        "user__username",
        "user__email",
        "phone",
    )


# ==========================
# COMPLAINT ADMIN
# ==========================

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "citizen",
        "category",
        "priority",
        "department",
        "status",
        "is_emergency",
        "created_at",
    )

    list_filter = (
        "category",
        "priority",
        "status",
        "is_emergency",
    )

    search_fields = (
        "title",
        "description",
        "location",
        "citizen__username",
    )

    list_editable = (
        "priority",
        "status",
        "department",
    )