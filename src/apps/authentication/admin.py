from django.contrib import admin

from .forms import CustomUserChangeForm, CustomUserCreateForm
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreateForm
    change_form = CustomUserChangeForm
    model = User
    list_display_links = ("username", "email")
    list_display = (
        "username",
        "email",
    )
    search_fields = ("username", "email")

    def get_fieldsets(self, request, obj=None):
        if not obj:
            self.fieldsets = (
                (None, {"classes": ("wide",), "fields": ("email", "username", "password", "is_staff", "is_active")}),
            )
        else:
            self.fieldsets = (
                (None, {"fields": ("email", "username", "password")}),
                ("Permissions", {"fields": ("is_staff", "is_active")}),
            )
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, change=False, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super().get_form(request, obj, **kwargs)
