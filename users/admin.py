from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "department")
    search_fields = ("user__username", "department")
    list_filter = ("department",)
    fieldsets = [
        (
            None,
            {
                "fields" : ["user", "department"],
            },
        ),
        (
            "Profile Details",
            {
                "fields": ["bio", "avatar"],
            }
        )
    ]
