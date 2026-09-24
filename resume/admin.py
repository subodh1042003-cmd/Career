from django.contrib import admin
from .models import Resume, TeamMember


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "predicted_domain",
        "confidence",
        "resume_score",
        "created_at",
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("name", "role")
