from django.db import models


class Resume(models.Model):

    name = models.CharField(
        max_length=200,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    resume_file = models.FileField(
        upload_to="resumes/"
    )

    extracted_text = models.TextField(
        blank=True
    )

    predicted_domain = models.CharField(
        max_length=200,
        blank=True
    )

    confidence = models.FloatField(
        default=0
    )

    resume_score = models.FloatField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name or "Resume"
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
