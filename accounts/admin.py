from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    AdminUserCreationForm,
    UserChangeForm,
)
from django.utils.translation import gettext_lazy as _
from .models import CustomUser,Profile

# ________________________________________________

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    form = UserChangeForm
    add_form = AdminUserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("email", "is_active", "is_admin")
    list_filter = ("is_admin", "is_superuser", "is_active", "groups")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    
admin.site.register(CustomUser,CustomUserAdmin)
# ________________________________________________

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user","first_name","last_name")
# ________________________________________________
