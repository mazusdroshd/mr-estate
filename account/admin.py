from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.models import CustomUser


class UserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = [
        'phone_number',
        'first_name',
        'last_name',
        'is_superuser'
    ]
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "address")}),
        ("Permissions", {"fields": ("is_active", "is_staff",
         "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "password1", "password2", "first_name", "last_name", "address", "is_staff")}
         ),
    )
    search_fields = ["phone_number"]
    ordering = ["phone_number"]


admin.site.register(CustomUser, UserAdmin)
